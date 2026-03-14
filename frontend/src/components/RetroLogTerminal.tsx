import React, { useEffect, useRef, useState, useMemo } from "react";

/**
 * RetroLogTerminal – A retro terminal-style component that renders
 * agent logs line-by-line with a typewriter animation, blinking cursor,
 * and a classic CRT-green scanline aesthetic.
 */

interface RetroLogTerminalProps {
    /** The full agent output text to animate */
    text: string;
    /** Speed in ms per character (default: 12) */
    speed?: number;
    /** Title shown in the terminal bar */
    title?: string;
}

const RetroLogTerminal: React.FC<RetroLogTerminalProps> = ({
    text,
    speed = 12,
    title = "AGENT OUTPUT",
}) => {
    const [displayed, setDisplayed] = useState("");
    const [done, setDone] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);
    const animRef = useRef<number | null>(null);

    // Memoize to avoid re-triggering on parent re-renders
    const stableText = useMemo(() => text, [text]);

    useEffect(() => {
        setDisplayed("");
        setDone(false);
        let i = 0;
        let lastTs = 0;

        const step = (ts: number) => {
            if (!lastTs) lastTs = ts;
            const elapsed = ts - lastTs;
            if (elapsed >= speed) {
                const charsToAdd = Math.min(
                    Math.floor(elapsed / speed),
                    stableText.length - i,
                    6 // max chars per frame for smooth feel
                );
                if (charsToAdd > 0) {
                    setDisplayed(stableText.slice(0, i + charsToAdd));
                    i += charsToAdd;
                    lastTs = ts;
                }
            }
            if (i < stableText.length) {
                animRef.current = requestAnimationFrame(step);
            } else {
                setDone(true);
            }
        };
        animRef.current = requestAnimationFrame(step);

        return () => {
            if (animRef.current) cancelAnimationFrame(animRef.current);
        };
    }, [stableText, speed]);

    // Auto-scroll as text appears
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [displayed]);

    return (
        <div className="retro-terminal">
            {/* Title bar */}
            <div className="retro-terminal-bar">
                <span className="retro-dot retro-dot--red" />
                <span className="retro-dot retro-dot--yellow" />
                <span className="retro-dot retro-dot--green" />
                <span className="retro-terminal-title">{title}</span>
            </div>

            {/* Body */}
            <div className="retro-terminal-body" ref={scrollRef}>
                <pre className="retro-terminal-text">
                    {displayed}
                    {!done && <span className="retro-cursor">▌</span>}
                </pre>
                {/* Scanline overlay */}
                <div className="retro-scanlines" />
            </div>
        </div>
    );
};

export default RetroLogTerminal;
