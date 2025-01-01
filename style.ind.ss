/* style.ind.css */
body {
    margin: 0;
    color: #333;
    background: linear-gradient(to bottom right, #e0eafc, #cfdef3); /* Subtle gradient background */
    overflow-x: hidden; /* Prevent horizontal scrollbar during animations */
}

.circuit-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        linear-gradient(90deg, transparent 98%, rgba(74, 144, 226, 0.1) 2%),
        linear-gradient(transparent 98%, rgba(74, 144, 226, 0.1) 2%);
    background-size: 50px 50px;
    z-index: -1;
    opacity: 0.3;
}

nav {
    position: fixed;
    width: 100%;
    top: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
    z-index: 100;
}

.nav-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-weight: 7;
}