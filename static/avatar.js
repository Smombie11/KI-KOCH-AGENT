import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const canvas = document.getElementById('avatarCanvas');
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(canvas.clientWidth, canvas.clientHeight);
renderer.setClearColor(0x1e1e1e);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
camera.position.set(0, 1.2, 2.5);
camera.lookAt(0, 1, 0);

// Beleuchtung
const ambientLight = new THREE.AmbientLight(0x404060);
scene.add(ambientLight);
const mainLight = new THREE.DirectionalLight(0xffffff, 1);
mainLight.position.set(2, 5, 3);
scene.add(mainLight);
const fillLight = new THREE.PointLight(0x4466cc, 0.3);
fillLight.position.set(0, -1, 1);
scene.add(fillLight);

// Bodenraster (optional)
const gridHelper = new THREE.GridHelper(5, 20, 0x888888, 0x444444);
gridHelper.position.y = -1.2;
scene.add(gridHelper);

// GLTFLoader – lädt VRM als einfaches 3D-Modell
const loader = new GLTFLoader();
loader.load('/static/models/Milk.vrm', (gltf) => {
    const model = gltf.scene;
    model.position.set(0, -0.9, 0);
    model.scale.set(2.2, 2.2, 2.2);
    scene.add(model);
    console.log('Avatar geladen (als GLTF)');
}, undefined, (error) => {
    console.error('Fehler beim Laden:', error);
});

// Größenanpassung
function resize() {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
}
resize();
window.addEventListener('resize', resize);

// Animation (kein VRM-Update nötig)
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();