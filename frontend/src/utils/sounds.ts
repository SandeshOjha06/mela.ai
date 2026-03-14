// Sound utility using Web Audio API — no external files needed
const ctx = () => new (window.AudioContext || (window as any).webkitAudioContext)();

function beep(freq: number, duration: number, type: OscillatorType = "sine", vol = 0.15) {
    try {
        const a = ctx();
        const o = a.createOscillator();
        const g = a.createGain();
        o.type = type;
        o.frequency.value = freq;
        g.gain.value = vol;
        o.connect(g);
        g.connect(a.destination);
        g.gain.exponentialRampToValueAtTime(0.001, a.currentTime + duration);
        o.start();
        o.stop(a.currentTime + duration);
    } catch { /* silent — AudioContext may not be available */ }
}

/** Soft chime for new chat messages */
export function playMessageSound() {
    beep(880, 0.12, "sine", 0.1);
    setTimeout(() => beep(1100, 0.1, "sine", 0.08), 80);
}

/** Alert tone for new problems */
export function playProblemSound() {
    beep(520, 0.15, "triangle", 0.15);
    setTimeout(() => beep(420, 0.2, "triangle", 0.12), 120);
}

/** Urgent dual-tone for emergencies */
export function playEmergencySound() {
    beep(800, 0.15, "square", 0.1);
    setTimeout(() => beep(600, 0.15, "square", 0.1), 150);
    setTimeout(() => beep(800, 0.15, "square", 0.1), 300);
}

/** Success chime for resolved problems */
export function playResolvedSound() {
    beep(660, 0.1, "sine", 0.1);
    setTimeout(() => beep(880, 0.1, "sine", 0.1), 100);
    setTimeout(() => beep(1100, 0.15, "sine", 0.08), 200);
}
