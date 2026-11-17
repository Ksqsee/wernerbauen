import React, { useEffect, useRef, useState } from 'react';

// Records a short voice message in the browser (MediaRecorder) and hands the result to the form as a File.
// Renders nothing on browsers without microphone recording support.

function pickType(): string {
  const MR: any = typeof window !== 'undefined' ? (window as any).MediaRecorder : null;
  if (!MR || !MR.isTypeSupported) return '';
  for (const t of ['audio/webm;codecs=opus', 'audio/mp4', 'audio/webm', 'audio/ogg;codecs=opus']) {
    if (MR.isTypeSupported(t)) return t;
  }
  return '';
}

function fmt(s: number) {
  const m = Math.floor(s / 60);
  const r = Math.floor(s % 60);
  return m + ':' + String(r).padStart(2, '0');
}

const Mic = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <rect x="9" y="3" width="6" height="11" rx="3" />
    <path d="M5 11a7 7 0 0 0 14 0" />
    <path d="M12 18v3" />
  </svg>
);

export default function VoiceNote({ value, onChange, label, hint, recordLabel, stopLabel, recordingLabel, deleteLabel, deniedText, fileHint, maxSeconds = 180, filePrefix = 'sprachnachricht', className = '', dark = false }: any) {
  const [supported, setSupported] = useState(false);
  const [rec, setRec] = useState(false);
  const [secs, setSecs] = useState(0);
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const mr = useRef<any>(null);
  const stream = useRef<MediaStream | null>(null);
  const timer = useRef<any>(null);

  const [fileMode, setFileMode] = useState(false);
  const fileRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    const doc: any = typeof document !== 'undefined' ? document : null;
    const pol: any = doc && (doc.permissionsPolicy || doc.featurePolicy);
    const blocked = !!(pol && pol.allowsFeature && !pol.allowsFeature('microphone'));
    const live = !!(typeof navigator !== 'undefined' && navigator.mediaDevices && navigator.mediaDevices.getUserMedia && pickType());
    setFileMode(blocked || !live);
    setSupported(true);
    return () => {
      if (timer.current) clearInterval(timer.current);
      if (stream.current) stream.current.getTracks().forEach((t) => t.stop());
    };
  }, []);

  useEffect(() => {
    if (!value) { setUrl(''); return; }
    const u = URL.createObjectURL(value);
    setUrl(u);
    return () => URL.revokeObjectURL(u);
  }, [value]);

  const stop = () => {
    if (timer.current) { clearInterval(timer.current); timer.current = null; }
    if (mr.current && mr.current.state !== 'inactive') mr.current.stop();
    setRec(false);
  };

  const start = async () => {
    setError('');
    try {
      const s = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.current = s;
      const type = pickType();
      const r = new (window as any).MediaRecorder(s, { mimeType: type });
      const chunks: BlobPart[] = [];
      r.ondataavailable = (e: any) => { if (e.data && e.data.size) chunks.push(e.data); };
      r.onstop = () => {
        s.getTracks().forEach((t) => t.stop());
        stream.current = null;
        const base = type.split(';')[0];
        const ext = base.indexOf('mp4') >= 0 ? 'm4a' : base.indexOf('ogg') >= 0 ? 'ogg' : 'webm';
        const stamp = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, '');
        if (chunks.length) onChange(new File(chunks, filePrefix + '-' + stamp + '.' + ext, { type: base }));
      };
      mr.current = r;
      r.start(1000);
      setSecs(0);
      setRec(true);
      const t0 = Date.now();
      timer.current = setInterval(() => {
        const sec = (Date.now() - t0) / 1000;
        setSecs(sec);
        if (sec >= Number(maxSeconds)) stop();
      }, 250);
    } catch (e: any) {
      setRec(false);
      if (e && (e.name === 'NotAllowedError' || e.name === 'SecurityError') && /policy|not allowed in this document/i.test(String(e.message || ''))) {
        setFileMode(true);
        if (fileRef.current) fileRef.current.click();
      } else setError(deniedText);
    }
  };

  if (!supported) return null;
  const hintText = fileMode && fileHint ? fileHint : hint;

  const box: React.CSSProperties = { display: 'flex', flexDirection: 'column', gap: 8 };
  const row: React.CSSProperties = { display: 'flex', alignItems: 'center', gap: 14, flexWrap: 'wrap', minHeight: 48 };
  const btn: React.CSSProperties = { position: 'relative', display: 'inline-flex', alignItems: 'center', gap: 10, height: 46, padding: '0 20px 0 14px', borderRadius: 12, border: dark ? '1.5px solid #ffffff33' : '1.5px solid #1D1D1B26', background: dark ? '#ffffff12' : '#ffffff', color: dark ? '#ffffff' : '#121212', font: 'inherit', fontSize: 15, fontWeight: 600, cursor: 'pointer' };
  const dot: React.CSSProperties = { width: 30, height: 30, borderRadius: '50%', background: 'var(--color-kit-key1, #D52625)', color: '#ffffff', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', flex: 'none' };
  const small: React.CSSProperties = { margin: 0, fontSize: 13, lineHeight: 1.5, color: dark ? '#ffffff99' : '#6b6b6b' };

  return (
    <div className={className} style={box}>
      {label ? <span style={{ fontSize: 14, fontWeight: 600, color: dark ? '#ffffffd9' : '#2b2b2b' }}>{label}</span> : null}
      <div style={row} aria-live="polite">
        {value && !rec ? (
          <>
            <audio controls src={url} preload="metadata" style={{ height: 44, maxWidth: '100%', flex: '1 1 220px' }} />
            <button type="button" style={{ ...btn, padding: '0 18px' }} onClick={() => onChange(null)}>{deleteLabel}</button>
          </>
        ) : rec ? (
          <>
            <button type="button" style={{ ...btn, borderColor: 'var(--color-kit-key1, #D52625)' }} onClick={stop}>
              <span style={{ ...dot, borderRadius: 6, width: 14, height: 14, margin: '0 8px' }} />
              {stopLabel}
            </button>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: 15, color: dark ? '#ffffff' : '#2b2b2b', fontVariantNumeric: 'tabular-nums' }}>
              <span style={{ width: 9, height: 9, borderRadius: '50%', background: 'var(--color-kit-key1, #D52625)', animation: 'gwvPulse 1.2s ease-in-out infinite' }} />
              {recordingLabel} {fmt(secs)} / {fmt(Number(maxSeconds))}
            </span>
            <style>{'@keyframes gwvPulse{0%,100%{opacity:1}50%{opacity:.25}}'}</style>
          </>
        ) : fileMode ? (
          <label style={btn}>
            <span style={dot}><Mic /></span>
            {recordLabel}
            <input
              ref={fileRef}
              type="file"
              accept="audio/*"
              {...({ capture: 'user' } as any)}
              style={{ position: 'absolute', width: 1, height: 1, opacity: 0, overflow: 'hidden', clip: 'rect(0 0 0 0)' }}
              onChange={(e) => { const f = e.target.files && e.target.files[0]; if (f) onChange(f); e.currentTarget.value = ''; }}
            />
          </label>
        ) : (
          <button type="button" style={btn} onClick={start}>
            <span style={dot}><Mic /></span>
            {recordLabel}
          </button>
        )}
      </div>
      {error ? <p style={{ ...small, color: 'var(--color-kit-key1, #D52625)' }} role="alert">{error}</p> : hintText ? <p style={small}>{hintText}</p> : null}
    </div>
  );
}
