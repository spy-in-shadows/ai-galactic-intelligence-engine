import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { gsap } from "gsap"

const planetMap = {}
const planets = []
const raycaster = new THREE.Raycaster()
const mouse = new THREE.Vector2()
window.addEventListener('mousemove', (event) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1
})

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

function createStarfield() {
  const starsGeometry = new THREE.BufferGeometry()
  const starCount = 5000

  const positions = new Float32Array(starCount * 3)

  for (let i = 0; i < starCount * 3; i++) {
    positions[i] = (Math.random() - 0.5) * 2000
  }

  starsGeometry.setAttribute(
    'position',
    new THREE.BufferAttribute(positions, 3)
  )

  const starsMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 1
  })

  const starField = new THREE.Points(starsGeometry, starsMaterial)
  scene.add(starField)
}

createStarfield()

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
    planets.push(sphere)
    planetMap[planet.name] = sphere
  })
}

loadPlanets()

function animate() {
  requestAnimationFrame(animate)
  controls.update()
  raycaster.setFromCamera(mouse, camera)
  const intersects = raycaster.intersectObjects(planets)

  planets.forEach(p => p.scale.set(1,1,1))

  if (intersects.length > 0) {
    intersects[0].object.scale.set(1.5,1.5,1.5)
  }
  renderer.render(scene, camera)
}

animate()

window.addEventListener('click', () => {
  raycaster.setFromCamera(mouse, camera)
  const intersects = raycaster.intersectObjects(planets)

  if (intersects.length > 0) {
    const planet = intersects[0].object

    const targetPosition = planet.position.clone().add(new THREE.Vector3(0, 0, 20))

    gsap.to(camera.position, {
      duration: 1.5,
      x: targetPosition.x,
      y: targetPosition.y,
      z: targetPosition.z,
    })
    document.getElementById("infoPanel").innerHTML = `
    <h3>${planet.userData.name}</h3>
    <p>Region: ${planet.userData.region}</p>
    `

    console.log("Selected:", planet.userData.name)
  }
})

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
})

document.getElementById("searchBtn").addEventListener("click", async () => {

  const query = document.getElementById("searchInput").value

  const response = await fetch(`http://127.0.0.1:8000/search?query=${query}`)
  const data = await response.json()

  highlightResults(data.results)
})


function highlightResults(results) {

  // Dim all planets
  planets.forEach(p => {
    p.material.opacity = 0.2
    p.material.transparent = true
  })

  if (results.length === 0) return

  const topPlanetName = results[0]
  const topPlanet = planetMap[topPlanetName]

  if (!topPlanet) return

  // Highlight top result
  topPlanet.material.opacity = 1
  topPlanet.material.color.set(0xff0000)

  // Focus camera
  const targetPosition = topPlanet.position.clone().add(new THREE.Vector3(0, 0, 20))

  gsap.to(camera.position, {
    duration: 1.5,
    x: targetPosition.x,
    y: targetPosition.y,
    z: targetPosition.z,
  })

  document.getElementById("infoPanel").innerHTML = `
    <h3>${topPlanetName}</h3>
    <p>AI Semantic Match</p>
  `
}