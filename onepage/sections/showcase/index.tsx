import React, { useEffect, useRef, useState } from 'react';
import { motion, useScroll, useTransform, useSpring, useMotionValueEvent } from 'framer-motion';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Showcase({ eyebrow, title, linkLabel, linkHref, cursorLabel, items }: any) {
  const list: any[] = (Array.isArray(items) ? items : []).filter((x: any) => x && x.image && x.image.src);
  const outer = useRef<HTMLDivElement | null>(null);
  const track = useRef<HTMLDivElement | null>(null);
  const [dist, setDist] = useState(0);
  const [wide, setWide] = useState(true);
  const [idx, setIdx] = useState(0);
  const [cur, setCur] = useState({ x: 0, y: 0, on: false });

  useEffect(() => {
    const measure = () => {
      const w = window.innerWidth;
      const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      setWide(w > 860 && !reduce);
      if (track.current) setDist(Math.max(0, track.current.scrollWidth - w + 64));
    };
    measure();
    window.addEventListener('resize', measure);
    const t = window.setTimeout(measure, 800);
    return () => { window.removeEventListener('resize', measure); window.clearTimeout(t); };
  }, [list.length]);

  const { scrollYProgress } = useScroll({ target: outer, offset: ['start start', 'end end'] });
  const smooth = useSpring(scrollYProgress, { stiffness: 120, damping: 30, mass: 0.4 });
  const x = useTransform(smooth, [0, 1], [0, -dist]);
  const bar = useTransform(smooth, [0, 1], ['0%', '100%']);
  useMotionValueEvent(scrollYProgress, 'change', (v) => {
    if (wide) setIdx(Math.min(list.length - 1, Math.round(v * (list.length - 1))));
  });

  const onScrollMobile = (e: React.UIEvent<HTMLDivElement>) => {
    const el = e.currentTarget;
    const max = el.scrollWidth - el.clientWidth;
    setIdx(max > 0 ? Math.round((el.scrollLeft / max) * (list.length - 1)) : 0);
  };

  const pad = (n: number) => String(n).padStart(2, '0');
  const head = (
    <div className={styles.head}>
      <div className={styles.headLeft}>
        {eyebrow ? <span className={styles.eyebrow}>{eyebrow}</span> : null}
        {title ? <h2 className={styles.title}>{title}</h2> : null}
      </div>
      <div className={styles.headRight}>
        <span className={styles.counter} aria-hidden="true"><b>{pad(idx + 1)}</b> / {pad(list.length)}</span>
        {linkLabel && linkHref ? <a className={styles.link} href={linkHref}>{linkLabel}<Icon name="arrow" size={16} /></a> : null}
      </div>
    </div>
  );

  const cards = list.map((p: any, i: number) => (
    <a
      key={i}
      href={p.href || linkHref}
      className={[styles.card, p.wide ? styles.cardWide : ''].join(' ')}
      onMouseEnter={() => setCur((c) => ({ ...c, on: true }))}
      onMouseLeave={() => setCur((c) => ({ ...c, on: false }))}
    >
      <span className={styles.media}>
        <Image src={p.image.src} alt={p.alt || p.title} className={styles.img} />
      </span>
      <span className={styles.meta}>
        <span className={styles.code}>R—{pad(i + 1)}</span>
        <span className={styles.cardTitle}>{p.title}</span>
        {p.category ? <span className={styles.cat}>{p.category}</span> : null}
      </span>
    </a>
  ));

  return (
    <section className={styles.section} onMouseMove={(e) => setCur((c) => ({ ...c, x: e.clientX, y: e.clientY }))}>
      <div ref={outer} className={styles.outer} style={wide ? { height: 'calc(100vh + ' + dist + 'px)' } : undefined}>
        {wide ? (
          <div className={styles.sticky}>
            {head}
            <motion.div ref={track} className={styles.track} style={{ x }}>{cards}</motion.div>
            <div className={styles.progress}><motion.span className={styles.progressFill} style={{ width: bar }} /></div>
          </div>
        ) : (
          <div className={styles.mobile}>
            {head}
            <div ref={track} className={styles.swipe} onScroll={onScrollMobile}>{cards}</div>
          </div>
        )}
      </div>
      {wide && cursorLabel ? (
        <span className={[styles.cursor, cur.on ? styles.cursorOn : ''].join(' ')} style={{ transform: 'translate(' + cur.x + 'px, ' + cur.y + 'px)' }} aria-hidden="true">
          <span className={styles.cursorDot}>{cursorLabel}</span>
        </span>
      ) : null}
    </section>
  );
}
