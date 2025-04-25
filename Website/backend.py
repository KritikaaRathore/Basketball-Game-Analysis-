<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Detected Basketball Video</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-gray-900 to-black text-white min-h-screen flex items-center justify-center p-6">
    <div class="bg-gray-800 p-10 rounded-2xl shadow-2xl w-full max-w-4xl border border-gray-700">
        <div class="text-center mb-6">
            <h1 class="text-3xl font-bold text-blue-400 flex justify-center items-center gap-2">
                <span>🏀 Detection Complete!</span>
            </h1>
            <p class="text-gray-300 mt-2">Your video has been analyzed. Watch the result below 👇</p>
        </div>

        <div class="rounded-xl overflow-hidden shadow-md mb-6">
            <video controls class="w-full rounded-lg border border-blue-500">
                <source src="{{ video_path }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>

        <div class="flex justify-center gap-6">
            <a href="{{ video_path }}" download class="bg-blue-600 hover:bg-blue-700 transition-all py-2 px-5 rounded-lg font-semibold shadow-md">
                ⬇️ Download Video
            </a>
            <a href="{{ url_for('index') }}" class="bg-gray-600 hover:bg-gray-700 transition-all py-2 px-5 rounded-lg font-semibold shadow-md">
                🔁 Upload Another
            </a>
        </div>
    </div>
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'935764818995673f',t:'MTc0NTUxNjQ5OC4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>
