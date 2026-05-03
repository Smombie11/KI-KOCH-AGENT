  import * as THREE from 'three';

const canvas = document.getElementById('avatarCanvas');
if (!canvas) {
    console.error('Canvas element not found!');
} else {
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
    renderer.setSize(canvas.clientWidth || 300, canvas.clientHeight || 300);
    renderer.setClearColor(0x1e1e1e);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
    camera.position.set(0, 0.5, 2.5);
    camera.lookAt(0, 0.8, 0);
    
    // Licht
    const ambient = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambient);
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(2, 5, 3);
    scene.add(dirLight);
    
    // Video-Element erstellen
    const video = document.createElement('video');
    video.src = '/static/models/avatar.mp4';
    video.loop = true;
    video.muted = true;
    video.autoplay = false;  // Nicht automatisch abspielen - wird von KI gesteuert
    video.playsInline = true;
    video.crossOrigin = "anonymous";
    video.style.display = 'none';
    document.body.appendChild(video);
    
    console.log('Video src:', video.src);
    
    // Video-Events
    video.addEventListener('loadstart', () => console.log('Video: loadstart'));
    video.addEventListener('canplay', () => console.log('Video: canplay'));
    video.addEventListener('canplaythrough', () => console.log('Video: canplaythrough'));
    video.addEventListener('play', () => console.log('Video: play'));
    video.addEventListener('error', (e) => console.error('Video error:', e));
    
    // Globale Funktionen für Avatar-Steuerung
    window.startAvatarVideo = () => {
        console.log('Avatar video started');
        video.currentTime = 0;
        video.play().catch(e => console.warn("Video play fehlgeschlagen:", e));
    };
    
    window.pauseAvatarVideo = () => {
        console.log('Avatar video paused');
        video.pause();
    };
    
    window.resumeAvatarVideo = () => {
        console.log('Avatar video resumed');
        video.play().catch(e => console.warn("Video resume fehlgeschlagen:", e));
    };
    
    window.stopAvatarVideo = () => {
        console.log('Avatar video stopped');
        video.pause();
        video.currentTime = 0;
    };
    
    // Textur aus Video
    const videoTexture = new THREE.VideoTexture(video);
    videoTexture.minFilter = THREE.LinearFilter;
    videoTexture.magFilter = THREE.LinearFilter;
    
    // Material mit Video-Textur - mit besserer Beleuchtung
    const material = new THREE.MeshStandardMaterial({ 
        map: videoTexture, 
        side: THREE.DoubleSide,
        metalness: 0,
        roughness: 0.5
    });
    
    // Plane (Rechteck) – größer für bessere Sichtbarkeit
    const geometry = new THREE.PlaneGeometry(2.2, 2.4);
    const videoPlane = new THREE.Mesh(geometry, material);
    videoPlane.position.set(0, 0.8, 0);
    scene.add(videoPlane);
    
    // Rahmen um das Video - eleganter Design
    const edgesGeo = new THREE.BoxGeometry(2.25, 2.45, 0.03);
    const edgesMat = new THREE.MeshStandardMaterial({ 
        color: 0x4CAF50, 
        metalness: 0.5, 
        roughness: 0.3,
        emissive: 0x2d7a3d,
        emissiveIntensity: 0.2
    });
    const frame = new THREE.Mesh(edgesGeo, edgesMat);
    frame.position.set(0, 0.8, -0.03);
    scene.add(frame);
    
    // Bodenraster
    const gridHelper = new THREE.GridHelper(5, 20, 0x888888, 0x444444);
    gridHelper.position.y = -0.5;
    scene.add(gridHelper);
    
    let lastTime = 0;
    function animate() {
        // Video-Textur aktualisieren wenn Video lädt
        if (video.readyState >= video.HAVE_CURRENT_DATA) {
            videoTexture.needsUpdate = true;
        }
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }
    animate();
    
    // Resize handler
    window.addEventListener('resize', () => {
        const width = canvas.clientWidth || 100;
        const height = canvas.clientHeight || 100;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    });
}