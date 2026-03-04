import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default {
    template: `
        <div style="position: absolute; left: 2%; bottom: 2%; width: 120px; height: 120px; pointer-events: none; z-index: 3;">
            <canvas ref="canvas"></canvas>
        </div>
    `,
    mounted() {
        this.$nextTick(() => {
            const canvas = this.$refs.canvas;
            this.renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
            this.renderer.setSize(120, 120);
            this.renderer.setClearColor(0x000000, 0);

            this.scene = new THREE.Scene();

            // Setup static orthogonal camera
            this.camera = new THREE.OrthographicCamera(-25, 25, 25, -25, 0.1, 500);
            this.camera.position.set(0, 0, 100);
            this.camera.lookAt(0, 0, 0);

            // Function to create sleek 3D arrow with glossy material
            const createAxis = (color, dir) => {
                const group = new THREE.Group();
                const length = 16;

                // Shaft
                const shaftGeo = new THREE.CylinderGeometry(0.8, 0.8, length, 16);
                const shaftMat = new THREE.MeshPhongMaterial({ color: color, shininess: 100 });
                const shaft = new THREE.Mesh(shaftGeo, shaftMat);
                shaft.position.copy(dir).multiplyScalar(length / 2);

                const defaultDir = new THREE.Vector3(0, 1, 0);
                const quaternion = new THREE.Quaternion().setFromUnitVectors(defaultDir, dir.clone().normalize());
                shaft.quaternion.copy(quaternion);
                group.add(shaft);

                // Tip - larger cone for classic axis look
                const coneGeo = new THREE.ConeGeometry(2.5, 7, 16);
                const coneMat = new THREE.MeshPhongMaterial({ color: color, shininess: 100 });
                const cone = new THREE.Mesh(coneGeo, coneMat);
                cone.position.copy(dir).multiplyScalar(length + 3.5);
                cone.quaternion.copy(quaternion);
                group.add(cone);

                return group;
            };

            const axesGroup = new THREE.Group();

            // X (Red), Y (Green), Z (Blue)
            const xAxis = createAxis(0xee3333, new THREE.Vector3(1, 0, 0));
            const yAxis = createAxis(0x33ee33, new THREE.Vector3(0, 1, 0));
            const zAxis = createAxis(0x3333ee, new THREE.Vector3(0, 0, 1));
            axesGroup.add(xAxis, yAxis, zAxis);

            // Center sphere focus dot
            const sphereGeo = new THREE.SphereGeometry(1.5, 16, 16);
            const sphereMat = new THREE.MeshPhongMaterial({ color: 0xdddd22, shininess: 100 });
            const centerSphere = new THREE.Mesh(sphereGeo, sphereMat);
            axesGroup.add(centerSphere);

            // 3 small white planes forming a corner as in the image
            const planeSize = 8;
            const planeGeo = new THREE.PlaneGeometry(planeSize, planeSize);
            const planeMat = new THREE.MeshPhongMaterial({
                color: 0xffffff,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.85,
                shininess: 50
            });

            const pXY = new THREE.Mesh(planeGeo, planeMat);
            pXY.position.set(planeSize / 2, planeSize / 2, 0);

            const pYZ = new THREE.Mesh(planeGeo, planeMat);
            pYZ.rotation.y = Math.PI / 2;
            pYZ.position.set(0, planeSize / 2, planeSize / 2);

            const pXZ = new THREE.Mesh(planeGeo, planeMat);
            pXZ.rotation.x = -Math.PI / 2;
            pXZ.position.set(planeSize / 2, 0, planeSize / 2);

            axesGroup.add(pXY, pYZ, pXZ);
            this.scene.add(axesGroup);

            // Add lighting
            const ambient = new THREE.AmbientLight(0xffffff, 0.6);
            this.scene.add(ambient);

            const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight1.position.set(50, 50, 50);
            this.scene.add(dirLight1);

            const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
            dirLight2.position.set(-50, -50, -50);
            this.scene.add(dirLight2);

            const sourceSceneId = this.sourceSceneId;
            let loggedError = false;
            let currentSourceVue = null;

            // Allow pointer events on our container for dragging
            this.$el.style.pointerEvents = 'auto';

            // Custom drag logic mapping to the source scene
            let isDragging = false;
            let lastMousePos = { x: 0, y: 0 };

            this._onMouseDown = (e) => {
                isDragging = true;
                lastMousePos = { x: e.clientX, y: e.clientY };
            };

            this._onMouseMove = (e) => {
                if (!isDragging || !currentSourceVue || !currentSourceVue.camera || !currentSourceVue.controls) return;

                const deltaX = e.clientX - lastMousePos.x;
                const deltaY = e.clientY - lastMousePos.y;
                lastMousePos = { x: e.clientX, y: e.clientY };

                const mainCamera = currentSourceVue.camera;
                const controls = currentSourceVue.controls;
                const target = controls.target;

                // Emulate OrbitControls rotation (adjust position in spherical coords)
                const offset = new THREE.Vector3().copy(mainCamera.position).sub(target);

                // Typical OrbitControls sensitivity
                const rotateSpeed = 0.01;

                // Spherical coordinates: theta is azimuth (around Y), phi is polar (from Y)
                // But NiceGUI overrides camera.up to (0,0,1), so Z is up, adjust accordingly
                const zUpOffset = new THREE.Vector3(offset.x, offset.z, -offset.y);
                const sp_zup = new THREE.Spherical().setFromVector3(zUpOffset);

                sp_zup.theta -= deltaX * rotateSpeed;
                sp_zup.phi -= deltaY * rotateSpeed;

                // Prevent flipping
                sp_zup.phi = Math.max(0.001, Math.min(Math.PI - 0.001, sp_zup.phi));

                // Safely update position back
                zUpOffset.setFromSpherical(sp_zup);
                offset.set(zUpOffset.x, -zUpOffset.z, zUpOffset.y);

                mainCamera.position.copy(target).add(offset);
                mainCamera.lookAt(target);
                // Also trigger controls so NiceGUI handles the event internally if needed
                controls.update();
            };

            this._onMouseUp = () => { isDragging = false; };
            this._onContextMenu = (e) => e.preventDefault();

            canvas.addEventListener('mousedown', this._onMouseDown);
            window.addEventListener('mousemove', this._onMouseMove);
            window.addEventListener('mouseup', this._onMouseUp);
            canvas.addEventListener('contextmenu', this._onContextMenu);

            const animate = () => {
                this.animationFrameId = requestAnimationFrame(animate);

                // Fetch the source scene Vue component natively using Vue 3 $refs
                const sourceVue = this.$root.$refs['r' + sourceSceneId];
                if (sourceVue && sourceVue.camera) {
                    currentSourceVue = sourceVue;
                    const mainCamera = sourceVue.camera;
                    // Mathematically invert the quaternion so the axesGroup rotates inside exactly like standard ViewHelper
                    // The ViewHelper camera remains fixed looking at (0,0,0)
                    axesGroup.quaternion.copy(mainCamera.quaternion).invert();
                } else if (!loggedError) {
                    console.warn(`ViewHelper: Cannot find source scene for ID 'c${sourceSceneId}'`);
                    loggedError = true;
                }

                this.renderer.render(this.scene, this.camera);
            };

            animate();
        });
    },
    beforeUnmount() {
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }

        if (this._onMouseMove) {
            window.removeEventListener('mousemove', this._onMouseMove);
        }
        if (this._onMouseUp) {
            window.removeEventListener('mouseup', this._onMouseUp);
        }

        if (this.$refs.canvas) {
            const canvas = this.$refs.canvas;
            if (this._onMouseDown) canvas.removeEventListener('mousedown', this._onMouseDown);
            if (this._onContextMenu) canvas.removeEventListener('contextmenu', this._onContextMenu);
        }

        if (this.renderer) {
            this.renderer.dispose();
            this.renderer.forceContextLoss();
        }

        // Traverse and dispose materials/geometries to prevent memory leaks in Three.js
        if (this.scene) {
            this.scene.traverse((object) => {
                if (object.isMesh) {
                    object.geometry.dispose();
                    if (object.material.isMaterial) {
                        object.material.dispose();
                    } else if (Array.isArray(object.material)) {
                        object.material.forEach(mat => mat.dispose());
                    }
                }
            });
        }
    },
    props: {
        sourceSceneId: Number
    }
}
