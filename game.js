class FastZoomGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Canvas setup
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        
        // Game state
        this.gameState = 'start'; // 'start', 'playing', 'end'
        this.currentRound = 1;
        this.totalRounds = 10;
        this.score = 0;
        this.timeLeft = 60;
        this.isZoomed = false;
        this.zoomLevel = 1;
        this.maxZoomLevel = 3;
        
        // Stats
        this.totalShots = 0;
        this.totalHits = 0;
        this.lastReactionTime = 0;
        this.reactionStartTime = 0;
        
        // Mouse position
        this.mouseX = 0;
        this.mouseY = 0;
        
        // Targets
        this.targets = [];
        this.maxTargets = 3;
        
        // Sound system
        this.soundEnabled = true;
        this.initSounds();
        
        // Weapon
        this.weapon = new Weapon(this);
        
        // UI elements
        this.ui = {
            timer: document.getElementById('timer'),
            round: document.getElementById('round'),
            score: document.getElementById('score'),
            reactionTime: document.getElementById('reactionTime'),
            accuracy: document.getElementById('accuracy'),
            zoomStatus: document.getElementById('zoomStatus'),
            crosshair: document.getElementById('crosshair'),
            startScreen: document.getElementById('startScreen'),
            endScreen: document.getElementById('endScreen'),
            finalScore: document.getElementById('finalScore'),
            leaderboardList: document.getElementById('leaderboardList')
        };
        
        // Timer
        this.gameTimer = null;
        
        this.setupEventListeners();
        this.loadLeaderboard();
    }
    
    initSounds() {
        // Create audio context for sound effects
        this.audioContext = null;
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch(e) {
            this.soundEnabled = false;
            console.log('Audio not supported');
        }
    }
    
    playSound(frequency, duration, type = 'sine') {
        if (!this.soundEnabled || !this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = type;
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
    
    playShootSound() {
        this.playSound(800, 0.1, 'square');
    }
    
    playHitSound() {
        this.playSound(1000, 0.2, 'triangle');
    }
    
    playZoomSound() {
        this.playSound(300, 0.1, 'sine');
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    setupEventListeners() {
        // Start button
        document.getElementById('startButton').addEventListener('click', () => {
            this.startGame();
        });
        
        // Replay button
        document.getElementById('replayButton').addEventListener('click', () => {
            this.resetGame();
            this.startGame();
        });
        
        // Mouse events
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouseX = e.clientX - rect.left;
            this.mouseY = e.clientY - rect.top;
            this.updateCrosshair();
        });
        
        this.canvas.addEventListener('mousedown', (e) => {
            e.preventDefault();
            if (this.gameState !== 'playing') return;
            
            if (e.button === 0) { // Left click - shoot
                this.weapon.shoot(this.mouseX, this.mouseY);
                this.playShootSound();
            } else if (e.button === 2) { // Right click - zoom
                this.weapon.startZoom();
                this.playZoomSound();
            }
        });
        
        this.canvas.addEventListener('mouseup', (e) => {
            if (e.button === 2) { // Right click release
                this.weapon.endZoom();
            }
        });
        
        // Prevent context menu
        this.canvas.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
        
        // Keyboard events
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && this.gameState === 'start') {
                this.startGame();
            }
        });
    }
    
    updateCrosshair() {
        if (this.isZoomed) {
            this.ui.crosshair.style.display = 'block';
            this.ui.crosshair.style.left = this.mouseX + 'px';
            this.ui.crosshair.style.top = this.mouseY + 'px';
        } else {
            this.ui.crosshair.style.display = 'none';
        }
    }
    
    startGame() {
        this.gameState = 'playing';
        this.ui.startScreen.style.display = 'none';
        this.ui.endScreen.style.display = 'none';
        
        this.resetRound();
        this.startRoundTimer();
        this.gameLoop();
    }
    
    resetGame() {
        this.currentRound = 1;
        this.score = 0;
        this.totalShots = 0;
        this.totalHits = 0;
        this.targets = [];
        this.updateUI();
    }
    
    resetRound() {
        this.timeLeft = 60;
        this.targets = [];
        this.reactionStartTime = Date.now();
        
        // Spawn initial targets
        this.spawnTargets();
    }
    
    startRoundTimer() {
        if (this.gameTimer) {
            clearInterval(this.gameTimer);
        }
        
        this.gameTimer = setInterval(() => {
            this.timeLeft--;
            this.updateUI();
            
            if (this.timeLeft <= 0) {
                this.endRound();
            }
        }, 1000);
    }
    
    endRound() {
        clearInterval(this.gameTimer);
        
        if (this.currentRound >= this.totalRounds) {
            this.endGame();
        } else {
            this.currentRound++;
            this.resetRound();
            this.startRoundTimer();
        }
    }
    
    endGame() {
        this.gameState = 'end';
        this.ui.endScreen.style.display = 'flex';
        this.ui.finalScore.textContent = `최종 점수: ${this.score}`;
        
        this.saveScore();
        this.displayLeaderboard();
    }
    
    spawnTargets() {
        const targetCount = Math.min(this.maxTargets, 1 + Math.floor(this.currentRound / 3));
        
        for (let i = 0; i < targetCount; i++) {
            setTimeout(() => {
                if (this.gameState === 'playing') {
                    this.targets.push(new Target(this, this.currentRound));
                }
            }, i * 800);
        }
    }
    
    removeTarget(target) {
        const index = this.targets.indexOf(target);
        if (index > -1) {
            this.targets.splice(index, 1);
            
            // Spawn new target after a delay
            setTimeout(() => {
                if (this.gameState === 'playing' && this.targets.length < this.maxTargets) {
                    this.targets.push(new Target(this, this.currentRound));
                }
            }, 800 + Math.random() * 1500);
        }
    }
    
    hitTarget(target) {
        this.totalHits++;
        this.score += target.points;
        this.lastReactionTime = Date.now() - this.reactionStartTime;
        this.reactionStartTime = Date.now();
        
        // Play hit sound
        this.playHitSound();
        
        // Add hit effect
        this.addHitEffect(target.x, target.y);
        
        this.removeTarget(target);
        this.updateUI();
    }
    
    addHitEffect(x, y) {
        // Create particle effect for hit
        const particles = [];
        for (let i = 0; i < 10; i++) {
            particles.push({
                x: x,
                y: y,
                dx: (Math.random() - 0.5) * 10,
                dy: (Math.random() - 0.5) * 10,
                life: 30,
                maxLife: 30
            });
        }
        
        const animateParticles = () => {
            this.ctx.save();
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                p.x += p.dx;
                p.y += p.dy;
                p.life--;
                
                if (p.life <= 0) {
                    particles.splice(i, 1);
                    continue;
                }
                
                const alpha = p.life / p.maxLife;
                this.ctx.globalAlpha = alpha;
                this.ctx.fillStyle = '#ff0000';
                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
                this.ctx.fill();
            }
            this.ctx.restore();
            
            if (particles.length > 0) {
                requestAnimationFrame(animateParticles);
            }
        };
        
        animateParticles();
    }
    
    updateUI() {
        this.ui.timer.textContent = this.timeLeft;
        this.ui.round.textContent = `${this.currentRound}/10`;
        this.ui.score.textContent = this.score;
        this.ui.reactionTime.textContent = `${this.lastReactionTime}ms`;
        
        const accuracy = this.totalShots > 0 ? Math.round((this.totalHits / this.totalShots) * 100) : 0;
        this.ui.accuracy.textContent = `${accuracy}%`;
        
        this.ui.zoomStatus.textContent = this.isZoomed ? 'ON' : 'OFF';
    }
    
    gameLoop() {
        if (this.gameState !== 'playing') return;
        
        this.update();
        this.render();
        
        requestAnimationFrame(() => this.gameLoop());
    }
    
    update() {
        // Update targets
        for (let i = this.targets.length - 1; i >= 0; i--) {
            this.targets[i].update();
            
            if (this.targets[i].shouldRemove) {
                this.targets.splice(i, 1);
                // Spawn replacement target
                setTimeout(() => {
                    if (this.gameState === 'playing' && this.targets.length < this.maxTargets) {
                        this.targets.push(new Target(this, this.currentRound));
                    }
                }, 500);
            }
        }
    }
    
    render() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw background
        this.drawBackground();
        
        // Apply zoom transform
        this.ctx.save();
        if (this.isZoomed) {
            this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);
            this.ctx.scale(this.zoomLevel, this.zoomLevel);
            this.ctx.translate(-this.mouseX, -this.mouseY);
        }
        
        // Draw targets
        this.targets.forEach(target => target.draw(this.ctx));
        
        this.ctx.restore();
        
        // Draw weapon/crosshair
        this.weapon.draw(this.ctx);
    }
    
    drawBackground() {
        // Sky gradient
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
        gradient.addColorStop(0, '#87CEEB');
        gradient.addColorStop(0.5, '#98FB98');
        gradient.addColorStop(1, '#8FBC8F');
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Simple ground
        this.ctx.fillStyle = '#654321';
        this.ctx.fillRect(0, this.canvas.height * 0.8, this.canvas.width, this.canvas.height * 0.2);
    }
    
    saveScore() {
        const playerName = prompt('이름을 입력하세요:') || 'Anonymous';
        const scores = this.getScores();
        
        scores.push({
            name: playerName,
            score: this.score,
            accuracy: this.totalShots > 0 ? Math.round((this.totalHits / this.totalShots) * 100) : 0,
            date: new Date().toLocaleDateString()
        });
        
        // Sort by score (descending) and keep top 10
        scores.sort((a, b) => b.score - a.score);
        scores.splice(10);
        
        localStorage.setItem('fastZoomScores', JSON.stringify(scores));
    }
    
    getScores() {
        const saved = localStorage.getItem('fastZoomScores');
        return saved ? JSON.parse(saved) : [];
    }
    
    loadLeaderboard() {
        this.displayLeaderboard();
    }
    
    displayLeaderboard() {
        const scores = this.getScores();
        const list = this.ui.leaderboardList;
        
        list.innerHTML = '';
        
        if (scores.length === 0) {
            list.innerHTML = '<div style="text-align: center; color: #666;">아직 기록이 없습니다</div>';
            return;
        }
        
        scores.forEach((score, index) => {
            const entry = document.createElement('div');
            entry.className = 'leaderboard-entry';
            entry.innerHTML = `
                <span>${index + 1}. ${score.name}</span>
                <span>${score.score}점 (${score.accuracy}%)</span>
            `;
            list.appendChild(entry);
        });
    }
}

class Weapon {
    constructor(game) {
        this.game = game;
        this.crosshairSize = 30;
    }
    
    startZoom() {
        this.game.isZoomed = true;
        this.game.zoomLevel = this.game.maxZoomLevel;
        this.game.updateCrosshair();
    }
    
    endZoom() {
        this.game.isZoomed = false;
        this.game.zoomLevel = 1;
        this.game.updateCrosshair();
    }
    
    shoot(x, y) {
        this.game.totalShots++;
        
        // Calculate accuracy based on zoom
        const accuracy = this.game.isZoomed ? 1.0 : 0.4;
        const spread = this.game.isZoomed ? 3 : 40;
        
        // Add spread to shot
        const actualX = x + (Math.random() - 0.5) * spread * (2 - accuracy);
        const actualY = y + (Math.random() - 0.5) * spread * (2 - accuracy);
        
        // Check for hits
        let hit = false;
        for (let target of this.game.targets) {
            if (target.checkHit(actualX, actualY)) {
                this.game.hitTarget(target);
                hit = true;
                break;
            }
        }
        
        // Add muzzle flash effect
        this.addMuzzleFlash(x, y);
        
        // End zoom after shooting
        if (this.game.isZoomed) {
            setTimeout(() => {
                this.endZoom();
            }, 100);
        }
        
        this.game.updateUI();
    }
    
    addMuzzleFlash(x, y) {
        // Simple muzzle flash effect
        const ctx = this.game.ctx;
        ctx.save();
        ctx.globalAlpha = 0.8;
        ctx.fillStyle = '#ffff00';
        ctx.beginPath();
        ctx.arc(x, y, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
    
    draw(ctx) {
        if (!this.game.isZoomed) {
            // Draw simple crosshair when not zoomed
            ctx.save();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 2;
            ctx.globalAlpha = 0.7;
            
            // Horizontal line
            ctx.beginPath();
            ctx.moveTo(this.game.mouseX - 15, this.game.mouseY);
            ctx.lineTo(this.game.mouseX + 15, this.game.mouseY);
            ctx.stroke();
            
            // Vertical line
            ctx.beginPath();
            ctx.moveTo(this.game.mouseX, this.game.mouseY - 15);
            ctx.lineTo(this.game.mouseX, this.game.mouseY + 15);
            ctx.stroke();
            
            ctx.restore();
        }
    }
}

class Target {
    constructor(game, round) {
        this.game = game;
        this.round = round;
        
        // Position
        this.x = Math.random() * (game.canvas.width - 100) + 50;
        this.y = Math.random() * (game.canvas.height * 0.6) + 100;
        
        // Size decreases with round
        this.baseSize = Math.max(25, 70 - round * 4);
        this.size = this.baseSize;
        
        // Speed increases with round
        this.speed = 0.8 + round * 0.4;
        this.dx = (Math.random() - 0.5) * this.speed;
        this.dy = (Math.random() - 0.5) * this.speed;
        
        // Target type affects points (smaller targets = more points)
        this.type = Math.floor(Math.random() * 3);
        const basePoints = [15, 25, 40][this.type];
        this.points = basePoints + Math.floor(round / 2) * 5; // Bonus points for higher rounds
        this.colors = ['#90EE90', '#FFA500', '#FF6347'][this.type];
        
        // Adjust size based on type (higher point targets are smaller)
        this.size = this.baseSize * [1.0, 0.8, 0.6][this.type];
        
        // Animation
        this.animationFrame = 0;
        
        // Lifespan decreases with round
        const baseLivespan = Math.max(3000, 6000 - round * 200); // 3-6 seconds
        this.lifespan = baseLivespan + Math.random() * 2000;
        this.creationTime = Date.now();
        this.shouldRemove = false;
    }
    
    update() {
        // Move
        this.x += this.dx;
        this.y += this.dy;
        
        // Bounce off walls
        if (this.x <= this.size || this.x >= this.game.canvas.width - this.size) {
            this.dx *= -1;
        }
        if (this.y <= this.size || this.y >= this.game.canvas.height * 0.8 - this.size) {
            this.dy *= -1;
        }
        
        // Keep in bounds
        this.x = Math.max(this.size, Math.min(this.game.canvas.width - this.size, this.x));
        this.y = Math.max(this.size, Math.min(this.game.canvas.height * 0.8 - this.size, this.y));
        
        // Animation
        this.animationFrame += 0.1;
        
        // Check lifespan
        if (Date.now() - this.creationTime > this.lifespan) {
            this.shouldRemove = true;
        }
    }
    
    draw(ctx) {
        ctx.save();
        
        // Pulsing effect
        const pulse = 1 + Math.sin(this.animationFrame) * 0.1;
        const currentSize = this.size * pulse;
        
        // Draw zombie-like target with better graphics
        ctx.fillStyle = this.colors;
        ctx.beginPath();
        ctx.arc(this.x, this.y, currentSize, 0, Math.PI * 2);
        ctx.fill();
        
        // Add shadow effect
        ctx.save();
        ctx.globalAlpha = 0.3;
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(this.x + 3, this.y + 3, currentSize, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
        
        // Draw face with more detail
        ctx.fillStyle = '#000';
        // Eyes (red for zombie effect)
        ctx.fillStyle = '#ff0000';
        ctx.beginPath();
        ctx.arc(this.x - currentSize * 0.3, this.y - currentSize * 0.2, currentSize * 0.08, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(this.x + currentSize * 0.3, this.y - currentSize * 0.2, currentSize * 0.08, 0, Math.PI * 2);
        ctx.fill();
        
        // Mouth (more menacing)
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.ellipse(this.x, this.y + currentSize * 0.3, currentSize * 0.25, currentSize * 0.15, 0, 0, Math.PI);
        ctx.fill();
        
        // Teeth
        ctx.fillStyle = '#fff';
        for (let i = 0; i < 3; i++) {
            const toothX = this.x - currentSize * 0.15 + i * currentSize * 0.15;
            ctx.fillRect(toothX, this.y + currentSize * 0.25, currentSize * 0.05, currentSize * 0.1);
        }
        
        // Points indicator
        ctx.fillStyle = '#fff';
        ctx.font = `${currentSize * 0.4}px Arial`;
        ctx.textAlign = 'center';
        ctx.fillText(this.points.toString(), this.x, this.y + currentSize * 0.1);
        
        // Health indicator (time left)
        const timeLeft = Math.max(0, (this.lifespan - (Date.now() - this.creationTime)) / this.lifespan);
        ctx.strokeStyle = timeLeft > 0.5 ? '#00ff00' : timeLeft > 0.2 ? '#ffff00' : '#ff0000';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(this.x, this.y, currentSize + 5, -Math.PI / 2, -Math.PI / 2 + (Math.PI * 2 * timeLeft));
        ctx.stroke();
        
        ctx.restore();
    }
    
    checkHit(x, y) {
        const distance = Math.sqrt((x - this.x) ** 2 + (y - this.y) ** 2);
        return distance <= this.size;
    }
}

// Initialize game when page loads
window.addEventListener('load', () => {
    new FastZoomGame();
});