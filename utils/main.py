-- 🔁 Updated main.py
import os
import cv2
import json
from utils import read_video
from trackers import PlayerTracker, BallTracker
from team_assigner import TeamAssigner
from court_keypoint_detector import CourtKeypointDetector
from ball_aquisition import BallAquisitionDetector
from pass_and_interception_detector import PassAndInterceptionDetector
from tactical_view_converter import TacticalViewConverter
from speed_and_distance_calculator import SpeedAndDistanceCalculator
from drawers import (
    PlayerTracksDrawer, BallTracksDrawer, CourtKeypointDrawer,
    TeamBallControlDrawer, FrameNumberDrawer, PassInterceptionDrawer,
    TacticalViewDrawer, SpeedAndDistanceDrawer
)
from configs import (
    STUBS_DEFAULT_PATH, PLAYER_DETECTOR_PATH,
    BALL_DETECTOR_PATH, COURT_KEYPOINT_DETECTOR_PATH
)

def save_video(frames, output_path, fps=30):
    if not frames:
        raise ValueError("❌ No frames to save. Please check the input video or processing steps.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)
    out.release()
    print(f"✅ Video saved successfully at: {output_path}")

    # Save thumbnail
    thumb_path = output_path.replace('.mp4', '_thumb.jpg')
    cv2.imwrite(thumb_path, frames[0])
    return thumb_path

def save_stats(passes, interceptions, speed_data, output_path):
    avg_speed = round(sum(sum(speed_data.values(), [])) / len(speed_data), 2) if speed_data else 0
    stats = {
        "total_passes": len(passes),
        "total_interceptions": len(interceptions),
        "average_speed": avg_speed
    }
    stats_path = output_path.replace('.mp4', '_stats.json')
    with open(stats_path, 'w') as f:
        json.dump(stats, f)
    return stats_path

def process_video(input_path, output_path):
    STUB_PATH = STUBS_DEFAULT_PATH
    video_frames = read_video(input_path)
    if not video_frames:
        print("❌ Error: No frames loaded.")
        return

    player_tracker = PlayerTracker(PLAYER_DETECTOR_PATH)
    ball_tracker = BallTracker(BALL_DETECTOR_PATH)
    court_keypoint_detector = CourtKeypointDetector(COURT_KEYPOINT_DETECTOR_PATH)

    player_tracks = player_tracker.get_object_tracks(video_frames, True, os.path.join(STUB_PATH, 'player_track_stubs.pkl'))
    ball_tracks = ball_tracker.get_object_tracks(video_frames, True, os.path.join(STUB_PATH, 'ball_track_stubs.pkl'))
    court_keypoints = court_keypoint_detector.get_court_keypoints(video_frames, True, os.path.join(STUB_PATH, 'court_key_points_stub.pkl'))

    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)

    team_assigner = TeamAssigner()
    player_assignment = team_assigner.get_player_teams_across_frames(video_frames, player_tracks, True, os.path.join(STUB_PATH, 'player_assignment_stub.pkl'))

    ball_aq = BallAquisitionDetector().detect_ball_possession(player_tracks, ball_tracks)
    pass_intercept = PassAndInterceptionDetector()
    passes = pass_intercept.detect_passes(ball_aq, player_assignment)
    interceptions = pass_intercept.detect_interceptions(ball_aq, player_assignment)

    tactical = TacticalViewConverter("./images/basketball_court.png")
    court_keypoints = tactical.validate_keypoints(court_keypoints)
    tactical_positions = tactical.transform_players_to_tactical_view(court_keypoints, player_tracks)

    dist_calc = SpeedAndDistanceCalculator(tactical.width, tactical.height, tactical.actual_width_in_meters, tactical.actual_height_in_meters)
    distances = dist_calc.calculate_distance(tactical_positions)
    speeds = dist_calc.calculate_speed(distances)

    drawers = [
        PlayerTracksDrawer(), BallTracksDrawer(), CourtKeypointDrawer(),
        TeamBallControlDrawer(), FrameNumberDrawer(), PassInterceptionDrawer(),
        SpeedAndDistanceDrawer(), TacticalViewDrawer()
    ]

    frames = video_frames
    frames = drawers[0].draw(frames, player_tracks, player_assignment, ball_aq)
    frames = drawers[1].draw(frames, ball_tracks)
    frames = drawers[2].draw(frames, court_keypoints)
    frames = drawers[3].draw(frames, player_assignment, ball_aq)
    frames = drawers[4].draw(frames)
    frames = drawers[5].draw(frames, passes, interceptions)
    frames = drawers[6].draw(frames, player_tracks, distances, speeds)
    frames = drawers[7].draw(frames, tactical.court_image_path, tactical.width, tactical.height, tactical.key_points, tactical_positions, player_assignment, ball_aq)

    thumb_path = save_video(frames, output_path)
    stats_path = save_stats(passes, interceptions, speeds, output_path)
    return thumb_path, stats_path
