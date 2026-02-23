import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

const scene = new THREE.Scene()
scene.background = new THREE.Color(0x000000)

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  2000
)

camera.position.z = 200

const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setSize(window.innerWidth, window.innerHeight)
document.body.appendChild(renderer.domElement)

const controls = new OrbitControls(camera, renderer.domElement)
controls.enableDamping = true

// Lighting
const light = new THREE.PointLight(0xffffff, 1.5)
light.position.set(100, 100, 100)
scene.add(light)

const ambient = new THREE.AmbientLight(0xffffff, 0.3)
scene.add(ambient)

// Fetch coordinates
async function loadPlanets() {
  const response = await fetch('http://127.0.0.1:8000/coordinates')
  const data = await response.json()

  data.forEach(planet => {
    const geometry = new THREE.SphereGeometry(3, 32, 32)

    let color
    if (planet.region === 0) color = 0xffff00
    else if (planet.region === 1) color = 0x00ffcc
    else color = 0xff0066

    const material = new THREE.MeshStandardMaterial({ color })
    const sphere = new THREE.Mesh(geometry, material)

    sphere.position.set(planet.x, planet.y, planet.z)
    sphere.userData = planet

    scene.add(sphere)
  })
}

loadPlanets()

function animate() {
  requestAnimationFrame(animate)
  controls.update()
  renderer.render(scene, camera)
}

animate()

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
})