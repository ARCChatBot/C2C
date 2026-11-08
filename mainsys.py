<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Classroom to Cleanroom (C2C) - Operation SEMI Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        vsuBlue: '#0047AB',
                        vsuOrange: '#FF6700',
                        vsuDark: '#1E293B',
                        vsuLight: '#F8FAFC'
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif']
                    }
                }
            }
        }
    </script>
    <!-- Google Fonts Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="h-full bg-vsuLight text-vsuDark font-sans antialiased flex flex-col">

    <!-- Top Navigation Header (VSU Blue, Orange, White) -->
    <header class="bg-vsuBlue border-b-4 border-vsuOrange sticky top-0 z-40 shadow-md text-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-24 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <div class="w-14 h-14 rounded-2xl bg-white text-vsuBlue flex items-center justify-center text-3xl font-extrabold shadow-inner border-2 border-vsuOrange">
                    <i class="fa-solid fa-graduation-cap"></i>
                </div>
                <div>
                    <h1 class="text-2xl font-extrabold tracking-tight flex items-center gap-2">
                        Classroom to Cleanroom <span class="text-[10px] uppercase px-2.5 py-1 bg-vsuOrange text-white rounded-full font-bold shadow-sm">C2C Pathway</span>
                    </h1>
                    <p class="text-xs text-blue-100 font-medium">Training system developed by <strong class="text-white underline">Operation SEMI (VSU)</strong></p>
                </div>
            </div>
            
            <div class="flex items-center space-x-6">
                <div class="hidden md:flex flex-col text-right">
                    <span class="text-xs font-bold text-white">Virginia State University</span>
                    <a href="https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2606117" target="_blank" class="text-[11px] text-amber-300 hover:underline font-semibold flex items-center gap-1 justify-end">
                        <i class="fa-solid fa-award"></i> NSF Award #2606117 <i class="fa-solid fa-external-link text-[9px]"></i>
                    </a>
                </div>
                <div class="w-11 h-11 rounded-full bg-vsuOrange text-white border-2 border-white flex items-center justify-center font-bold text-base shadow-lg">
                    <i class="fa-solid fa-microchip"></i>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Dashboard Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col gap-8 pb-24">

        <!-- Grant About Section (Award Abstract # 2606117) -->
        <section class="bg-white rounded-3xl p-8 border-2 border-vsuBlue/20 shadow-xl relative overflow-hidden">
            <div class="absolute top-0 right-0 w-32 h-32 bg-vsuOrange/10 rounded-bl-full pointer-events-none"></div>
            <div class="flex items-center gap-3 mb-4">
                <div class="w-10 h-10 rounded-xl bg-blue-50 text-vsuBlue flex items-center justify-center text-lg font-bold border border-blue-200">
                    <i class="fa-solid fa-book-bookmark"></i>
                </div>
                <div>
                    <span class="text-xs font-bold text-vsuOrange uppercase tracking-wider">National Science Foundation Grant</span>
                    <h2 class="text-xl font-extrabold text-vsuDark">About the Grant &bull; Award Abstract # 2606117</h2>
                </div>
            </div>
            <div class="bg-vsuLight p-6 rounded-2xl border border-slate-200">
                <p class="text-slate-700 text-sm md:text-base leading-relaxed font-medium mb-4">
                    <strong>Targeted Infusion Project:</strong> Enhancing Undergraduate Education and Research in AI-Driven Microelectronics at Virginia State University through the <strong>Classroom to Cleanroom (C2C) Pathway</strong>.
                </p>
                <div class="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-200">
                    <span class="text-xs text-slate-500 font-semibold"><i class="fa-solid fa-university text-vsuBlue"></i> Host Institution: Virginia State University (VSU)</span>
                    <a href="https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2606117" target="_blank" class="px-4 py-2 bg-vsuBlue hover:bg-blue-800 text-white font-bold text-xs rounded-xl shadow-md transition-colors flex items-center gap-2">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i> View Official NSF Award Record
                    </a>
                </div>
            </div>
        </section>

        <!-- System Architecture & Interaction Layers -->
        <div class="space-y-4">
            <h3 class="text-xl font-extrabold text-vsuDark flex items-center gap-2">
                <i class="fa-solid fa-layer-group text-vsuOrange"></i> C2C Training Management System Architecture
            </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

            <!-- Layer 1: Computer-Based Training Node -->
            <div class="bg-white rounded-3xl p-6 border-t-4 border-vsuBlue border-x border-b border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
                <div>
                    <div class="w-12 h-12 rounded-2xl bg-blue-50 text-vsuBlue flex items-center justify-center text-xl font-bold mb-4 border border-blue-100">
                        <i class="fa-solid fa-desktop"></i>
                    </div>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-vsuBlue bg-blue-50 px-2.5 py-1 rounded-full">Layer 01</span>
                    <h4 class="text-lg font-bold text-vsuDark mt-3 mb-2">Computer-Based Training Node</h4>
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">
                        Interactive digital modules delivering foundational knowledge, AI literacy, and core microelectronics concepts.
                    </p>
                </div>
                <div>
                    <a href="https://c2c-5y77.onrender.com/cbt" target="_blank" class="w-full mb-3 py-2.5 bg-vsuBlue hover:bg-blue-800 text-white font-bold text-xs rounded-xl shadow transition-colors flex items-center justify-center gap-2">
                        <i class="fa-solid fa-play"></i> Launch CBT Portal
                    </a>
                    <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-slate-400 font-medium">Platform Status</span>
                        <span class="text-emerald-600 font-bold">Active</span>
                    </div>
                </div>
            </div>

            <!-- Layer 2: 3D Simulation Microelectronics Training Node -->
            <div class="bg-white rounded-3xl p-6 border-t-4 border-vsuOrange border-x border-b border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
                <div>
                    <div class="w-12 h-12 rounded-2xl bg-orange-50 text-vsuOrange flex items-center justify-center text-xl font-bold mb-4 border border-orange-100">
                        <i class="fa-solid fa-cubes"></i>
                    </div>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-vsuOrange bg-orange-50 px-2.5 py-1 rounded-full">Layer 02</span>
                    <h4 class="text-lg font-bold text-vsuDark mt-3 mb-2">3D Simulation Training Node</h4>
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">
                        Immersive 3D environments simulating semiconductor fabrication processes and microelectronic equipment mechanics.
                    </p>
                </div>
                <div>
                    <button onclick="alert('Launching 3D Microelectronics Simulation Sandbox...')" class="w-full mb-3 py-2.5 bg-vsuOrange hover:bg-orange-600 text-white font-bold text-xs rounded-xl shadow transition-colors flex items-center justify-center gap-2">
                        <i class="fa-solid fa-cube"></i> Open 3D Simulator
                    </button>
                    <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-slate-400 font-medium">Environment</span>
                        <span class="text-vsuOrange font-bold">Interactive 3D</span>
                    </div>
                </div>
            </div>

            <!-- Layer 3: Virtual Reality Cleanroom Training Node -->
            <div class="bg-white rounded-3xl p-6 border-t-4 border-vsuBlue border-x border-b border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
                <div>
                    <div class="w-12 h-12 rounded-2xl bg-blue-50 text-vsuBlue flex items-center justify-center text-xl font-bold mb-4 border border-blue-100">
                        <i class="fa-solid fa-vr-cardboard"></i>
                    </div>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-vsuBlue bg-blue-50 px-2.5 py-1 rounded-full">Layer 03</span>
                    <h4 class="text-lg font-bold text-vsuDark mt-3 mb-2">VR Cleanroom Training Node</h4>
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">
                        Virtual Reality integration guiding students through cleanroom protocols, safety guidelines, and tool operation.
                    </p>
                </div>
                <div>
                    <button onclick="alert('Initializing VR Cleanroom Headset Bridge & Stream...')" class="w-full mb-3 py-2.5 bg-vsuBlue hover:bg-blue-800 text-white font-bold text-xs rounded-xl shadow transition-colors flex items-center justify-center gap-2">
                        <i class="fa-solid fa-headset"></i> Launch VR Portal
                    </button>
                    <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-slate-400 font-medium">Technology</span>
                        <span class="text-vsuBlue font-bold">VR Immersive</span>
                    </div>
                </div>
            </div>

            <!-- Layer 4: SOP and Training Documentation Repository -->
            <div class="bg-white rounded-3xl p-6 border-t-4 border-vsuOrange border-x border-b border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
                <div>
                    <div class="w-12 h-12 rounded-2xl bg-orange-50 text-vsuOrange flex items-center justify-center text-xl font-bold mb-4 border border-orange-100">
                        <i class="fa-solid fa-folder-open"></i>
                    </div>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-vsuOrange bg-orange-50 px-2.5 py-1 rounded-full">Layer 04</span>
                    <h4 class="text-lg font-bold text-vsuDark mt-3 mb-2">SOP & Documentation Repository</h4>
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">
                        Centralized repository for Standard Operating Procedures (SOPs), safety guidelines, and training materials.
                    </p>
                </div>
                <div>
                    <button onclick="alert('Opening secure SOP & Document Archive...')" class="w-full mb-3 py-2.5 bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs rounded-xl shadow transition-colors flex items-center justify-center gap-2">
                        <i class="fa-solid fa-file-lines"></i> View Repository
                    </button>
                    <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-slate-400 font-medium">Access</span>
                        <span class="text-vsuOrange font-bold">Secure Cloud</span>
                    </div>
                </div>
            </div>

            <!-- Layer 5: Physical Equipment Training & Scheduling Node -->
            <div class="bg-white rounded-3xl p-6 border-t-4 border-vsuBlue border-x border-b border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between lg:col-span-2">
                <div>
                    <div class="w-12 h-12 rounded-2xl bg-blue-50 text-vsuBlue flex items-center justify-center text-xl font-bold mb-4 border border-blue-100">
                        <i class="fa-solid fa-screwdriver-wrench"></i>
                    </div>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-vsuBlue bg-blue-50 px-2.5 py-1 rounded-full">Layer 05</span>
                    <h4 class="text-lg font-bold text-vsuDark mt-3 mb-3">Physical Equipment Training &amp; Scheduling</h4>
                    
                    <div class="space-y-3 text-xs text-slate-700 bg-vsuLight p-4 rounded-2xl border border-slate-200 mb-4">
                        <div class="flex items-start gap-2.5">
                            <span class="w-5 h-5 rounded-full bg-vsuBlue text-white font-bold flex items-center justify-center shrink-0 text-[10px]">1</span>
                            <div>
                                <strong class="text-slate-900 block">Review Available Training Times:</strong>
                                <span class="text-slate-600">Sessions are held Tuesdays &amp; Thursdays from 3:30 PM – 4:50 PM EST.</span>
                            </div>
                        </div>
                        <div class="flex items-start gap-2.5">
                            <span class="w-5 h-5 rounded-full bg-vsuBlue text-white font-bold flex items-center justify-center shrink-0 text-[10px]">2</span>
                            <div>
                                <strong class="text-slate-900 block">Confirm Target Equipment:</strong>
                                <span class="text-slate-600">Digital Multimeter, HoloLens 2, VR Oculus 2, Enderbot 3D Printer, or NVIDIA Jetson Nano.</span>
                            </div>
                        </div>
                        <div class="flex items-start gap-2.5">
                            <span class="w-5 h-5 rounded-full bg-vsuBlue text-white font-bold flex items-center justify-center shrink-0 text-[10px]">3</span>
                            <div>
                                <strong class="text-slate-900 block">Select a Student Mentor:</strong>
                                <span class="text-slate-600">Choose your assigned peer mentor from Operation SEMI to guide your hands-on session.</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <button onclick="openEquipmentModal()" class="w-full mb-3 py-2.5 bg-vsuBlue hover:bg-blue-800 text-white font-bold text-xs rounded-xl shadow transition-colors flex items-center justify-center gap-2">
                        <i class="fa-solid fa-calendar-check"></i> Schedule Equipment Training
                    </button>
                    <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="text-slate-400 font-medium">Lab Availability</span>
                        <span class="text-emerald-600 font-bold">Open for Booking</span>
                    </div>
                </div>
            </div>

        </div>

        <!-- Project Gallery Section -->
        <section class="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
            <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
                <div class="w-10 h-10 rounded-xl bg-blue-50 text-vsuBlue flex items-center justify-center text-lg font-bold border border-blue-200">
                    <i class="fa-solid fa-images"></i>
                </div>
                <div>
                    <span class="text-xs font-bold text-vsuOrange uppercase tracking-wider">Visual Assets &amp; Lab Media</span>
                    <h2 class="text-xl font-extrabold text-vsuDark">C2C Pathway Gallery</h2>
                </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <!-- Gallery Item 1 -->
                <div class="group relative bg-vsuLight rounded-2xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition-all">
                    <img src="https://placehold.co/600x400/0047AB/FFFFFF?text=Cleanroom+Protocol+VR" alt="Cleanroom Protocol VR" class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
                    <div class="p-4">
                        <span class="text-[10px] font-bold text-vsuOrange uppercase bg-orange-50 px-2 py-0.5 rounded-full">Virtual Reality</span>
                        <h4 class="text-sm font-extrabold text-vsuDark mt-1">Gowning &amp; Safety Protocol Simulation</h4>
                    </div>
                </div>
                <!-- Gallery Item 2 -->
                <div class="group relative bg-vsuLight rounded-2xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition-all">
                    <img src="https://placehold.co/600x400/FF6700/FFFFFF?text=3D+Wafer+Fabrication" alt="3D Wafer Fabrication" class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
                    <div class="p-4">
                        <span class="text-[10px] font-bold text-vsuBlue uppercase bg-blue-50 px-2.5 py-0.5 rounded-full">3D Simulation</span>
                        <h4 class="text-sm font-extrabold text-vsuDark mt-1">Photolithography &amp; Etching Simulator</h4>
                    </div>
                </div>
                <!-- Gallery Item 3 -->
                <div class="group relative bg-vsuLight rounded-2xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition-all">
                    <img src="https://placehold.co/600x400/1E293B/FFFFFF?text=AI+Dashboard+CBT" alt="AI Dashboard CBT" class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
                    <div class="p-4">
                        <span class="text-[10px] font-bold text-vsuOrange uppercase bg-orange-50 px-2 py-0.5 rounded-full">Computer-Based Training</span>
                        <h4 class="text-sm font-extrabold text-vsuDark mt-1">AI-Driven Microelectronics Analytics</h4>
                    </div>
                </div>
                <!-- Gallery Item 4 -->
                <div class="group relative bg-vsuLight rounded-2xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition-all">
                    <img src="IMG_0185.jpg" alt="Micron Sponsorship Engagement and Operation SEMI Team Visit" class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300" onerror="this.onerror=null; this.src='https://placehold.co/600x400/0047AB/FFFFFF?text=Micron+Sponsorship+Visit';">
                    <div class="p-4">
                        <span class="text-[10px] font-bold text-vsuBlue uppercase bg-blue-50 px-2.5 py-0.5 rounded-full">Sponsorship Engagement</span>
                        <h4 class="text-sm font-extrabold text-vsuDark mt-1">Micron Technology Visit &bull; Hosted by Operation SEMI</h4>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- About the Team Section -->
        <section class="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
            <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
                <div class="w-10 h-10 rounded-xl bg-orange-50 text-vsuOrange flex items-center justify-center text-lg font-bold border border-orange-200">
                    <i class="fa-solid fa-users-gear"></i>
                </div>
                <div>
                    <span class="text-xs font-bold text-vsuOrange uppercase tracking-wider">Collaboration & Leadership</span>
                    <h2 class="text-xl font-extrabold text-vsuDark">About the Team &bull; C2C Pathway &amp; Operation SEMI</h2>
                </div>
            </div>

            <!-- Advisors Slots -->
            <div class="mb-8 bg-vsuLight p-6 rounded-2xl border border-slate-200">
                <h3 class="text-sm font-extrabold uppercase tracking-wider text-vsuBlue mb-3 flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user"></i> Faculty Advisors
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-blue-100 text-vsuBlue flex items-center justify-center font-bold">
                            <i class="fa-solid fa-user-tie"></i>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-slate-400 uppercase block">Co-Principal Investigator (Co-PI)</span>
                            <span class="text-sm font-extrabold text-vsuDark">Dr. Peng Cheng</span>
                        </div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-blue-100 text-vsuBlue flex items-center justify-center font-bold">
                            <i class="fa-solid fa-user-tie"></i>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-slate-400 uppercase block">Co-Principal Investigator (Co-PI)</span>
                            <span class="text-sm font-extrabold text-vsuDark">Dr. Tao Sun</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- About Us - Student Section -->
            <div class="mb-8 bg-gradient-to-r from-blue-50 to-orange-50 p-6 rounded-2xl border border-blue-100">
                <div class="flex items-center gap-2 mb-2">
                    <i class="fa-solid fa-user-graduate text-vsuBlue"></i>
                    <h3 class="text-sm font-extrabold uppercase tracking-wider text-vsuBlue">About Us &bull; Student Engineering Cohort</h3>
                </div>
                <p class="text-xs md:text-sm text-slate-700 leading-relaxed font-medium">
                    Our multidisciplinary student team brings together top undergraduate and research talent from Virginia State University and Virginia Tech, partnering with Operation SEMI. Together, we are designing, developing, and deploying next-generation AI-driven microelectronics training modules, interactive 3D simulations, and immersive virtual reality cleanroom environments to prepare the future semiconductor workforce.
                </p>
            </div>

            <!-- Three Teams Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Operation SEMI (VSU) Team -->
                <div class="bg-white rounded-2xl p-6 border-t-4 border-vsuOrange border-x border-b border-slate-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="text-base font-extrabold text-vsuDark">Operation SEMI (VSU)</h4>
                            <span class="text-[10px] bg-orange-100 text-vsuOrange font-bold px-2.5 py-0.5 rounded-full">AI System Engineering</span>
                        </div>
                        <ul class="space-y-2 text-xs text-slate-700 mt-4">
                            <li class="flex items-center justify-between p-2 rounded-lg bg-slate-50 font-semibold">
                                <span>Nicolas Pollard</span>
                                <span class="text-[10px] text-vsuOrange font-bold">Team Lead</span>
                            </li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Tory'elle Coleman</li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Larry Caldwell</li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Sabien Hill</li>
                        </ul>
                    </div>
                </div>

                <!-- Virginia Tech Team -->
                <div class="bg-white rounded-2xl p-6 border-t-4 border-vsuBlue border-x border-b border-slate-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="text-base font-extrabold text-vsuDark">Virginia Tech (VT)</h4>
                            <span class="text-[10px] bg-blue-100 text-vsuBlue font-bold px-2.5 py-0.5 rounded-full">VR Cleanroom Design</span>
                        </div>
                        <ul class="space-y-2 text-xs text-slate-700 mt-4">
                            <li class="flex items-center justify-between p-2 rounded-lg bg-slate-50 font-semibold">
                                <span>Kayin Buckley</span>
                                <span class="text-[10px] text-vsuBlue font-bold">Team Lead</span>
                            </li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Darwin Octchere</li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Fiorenza Viacava</li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Jacob Enslen</li>
                        </ul>
                    </div>
                </div>

                <!-- VSU Team -->
                <div class="bg-white rounded-2xl p-6 border-t-4 border-vsuOrange border-x border-b border-slate-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="text-base font-extrabold text-vsuDark">Virginia State University (VSU)</h4>
                            <span class="text-[10px] bg-orange-100 text-vsuOrange font-bold px-2.5 py-0.5 rounded-full">VR Training Modules</span>
                        </div>
                        <ul class="space-y-2 text-xs text-slate-700 mt-4">
                            <li class="flex items-center justify-between p-2 rounded-lg bg-slate-50 font-semibold">
                                <span>Keasara Etienne</span>
                                <span class="text-[10px] text-vsuOrange font-bold">Team Lead</span>
                            </li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Jalen Wooden</li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Trey [Last Name]</li>
                            <li class="p-2 rounded-lg bg-white border border-slate-100">Geoff [Last Name]</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- Equipment Scheduling Modal -->
    <div id="equipmentModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-3xl max-w-lg w-full p-8 shadow-2xl border border-slate-100 space-y-6">
            <div class="flex items-center justify-between pb-4 border-b border-slate-100">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-blue-50 text-vsuBlue flex items-center justify-center text-lg font-bold border border-blue-200">
                        <i class="fa-solid fa-calendar-days"></i>
                    </div>
                    <h3 class="text-lg font-extrabold text-vsuDark">Physical Equipment Booking</h3>
                </div>
                <button onclick="closeEquipmentModal()" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            
            <form id="equipmentForm" onsubmit="submitEquipmentBooking(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Student ID</label>
                    <input type="text" id="eqStudentId" placeholder="e.g. VSU-100294" required class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-vsuBlue bg-slate-50">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Select Training Time Slot</label>
                    <select id="eqTimeSlot" required class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-vsuBlue bg-slate-50">
                        <option value="">-- Choose Tuesday / Thursday Slot --</option>
                        <option value="Tuesday 3:30 PM - 4:50 PM EST">Tuesday | 3:30 PM - 4:50 PM EST</option>
                        <option value="Thursday 3:30 PM - 4:50 PM EST">Thursday | 3:30 PM - 4:50 PM EST</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Target Equipment</label>
                    <select id="eqTarget" required class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-vsuBlue bg-slate-50">
                        <option value="">-- Select Equipment --</option>
                        <option value="Digital Multimeter">Digital Multimeter</option>
                        <option value="HoloLens 2 equipment">HoloLens 2 equipment</option>
                        <option value="VR Oculus 2">VR Oculus 2</option>
                        <option value="Enderbot 3D printer">Enderbot 3D printer</option>
                        <option value="Nvidia Jetson Nano">Nvidia Jetson Nano</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Assigned Student Mentor</label>
                    <select id="eqMentor" required class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-vsuBlue bg-slate-50">
                        <option value="">-- Select Student Mentor --</option>
                        <option value="Nicolas Pollard (Operation SEMI Lead)">Nicolas Pollard (Operation SEMI Lead)</option>
                        <option value="Tory'elle Coleman">Tory'elle Coleman</option>
                        <option value="Larry Caldwell">Larry Caldwell</option>
                        <option value="Sabien Hill">Sabien Hill</option>
                        <option value="Kayin Buckley (VT Lead)">Kayin Buckley (VT Lead)</option>
                        <option value="Keasara Etienne (VSU Lead)">Keasara Etienne (VSU Lead)</option>
                    </select>
                </div>
                <button type="submit" class="w-full py-3 px-4 rounded-xl bg-vsuBlue hover:bg-blue-800 text-white font-bold text-sm shadow-md transition-colors flex items-center justify-center gap-2 mt-2">
                    <i class="fa-solid fa-check"></i> Confirm &amp; Log Equipment Session
                </button>
            </form>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-vsuBlue text-white border-t-2 border-vsuOrange py-6 text-center text-xs">
        <p>Virginia State University &bull; Classroom to Cleanroom (C2C) &bull; Developed by Operation SEMI (VSU) &bull; NSF Award #2606117</p>
    </footer>

    <!-- Equipment Booking Logic -->
    <script>
        function openEquipmentModal() {
            document.getElementById('equipmentModal').classList.remove('hidden');
        }

        function closeEquipmentModal() {
            document.getElementById('equipmentModal').classList.add('hidden');
        }

        async function submitEquipmentBooking(event) {
            event.preventDefault();
            const studentId = document.getElementById('eqStudentId').value.trim();
            const timeSlot = document.getElementById('eqTimeSlot').value;
            const equipment = document.getElementById('eqTarget').value;
            const mentor = document.getElementById('eqMentor').value;

            try {
                const response = await fetch('https://c2c-5y77.onrender.com/api/complete-training', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        student_id: studentId,
                        score: 100.0,
                        track: `Physical Equipment - ${equipment} w/ ${mentor} (${timeSlot})`
                    })
                });

                if (response.ok) {
                    alert('Equipment training session successfully booked and logged!');
                    closeEquipmentModal();
                } else {
                    alert('Failed to log equipment session.');
                }
            } catch (err) {
                console.error('Connection error:', err);
                alert('Could not connect to Render backend.');
            }
        }
    </script>
</body>
</html>
