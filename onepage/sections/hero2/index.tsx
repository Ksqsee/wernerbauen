import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

const EASE = [0.22, 1, 0.36, 1];

export default function Hero2({ eyebrow, headline, accent, sub, primaryLabel, primaryHref, secondaryLabel, secondaryHref, trust, slides, interval }: any) {
  const list: any[] = (Array.isArray(slides) ? slides : []).filter((s: any) => s && s.image && s.image.src);
  const trustList: string[] = String(trust || '').split('\n').map((t) => t.trim()).filter(Boolean);
  const [active, setActive] = useState(0);
  const [still, setStill] = useState(false);
  const secs = Math.max(4, Number(interval) || 7);

  useEffect(() => {
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    setStill(!!reduce);
    if (reduce || list.length < 2) return;
    const t = window.setTimeout(() => setActive((a) => (a + 1) % list.length), secs * 1000);
    return () => window.clearTimeout(t);
  }, [active, list.length, secs]);

  const words = (t: string, delay: number) =>
    String(t || '').split(' ').map((w, i) => (
      <React.Fragment key={i}>
        {i > 0 ? ' ' : null}
        <span className={styles.wordWrap}>
          <motion.span className={styles.word} initial={{ y: '110%' }} animate={{ y: 0 }} transition={{ duration: 0.9, ease: EASE, delay: delay + i * 0.06 }}>{w}</motion.span>
        </span>
      </React.Fragment>
    ));

  return (
    <section className={styles.hero} style={{ ['--secs' as any]: secs + 's' }}>
      <div className={styles.media}>
        {list.map((s: any, i: number) => (
          <div key={i} className={[styles.slide, i === active ? styles.slideOn : '', still ? styles.still : ''].join(' ')} aria-hidden={i === active ? undefined : true}>
            <Image src={s.image.src} alt={s.alt} className={styles.img} />
          </div>
        ))}
        <div className={styles.shade} aria-hidden="true" />
      </div>

      <div className={styles.inner}>
        <div className={styles.copy}>
          {eyebrow ? (
            <motion.p className={styles.eyebrow} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8, delay: 0.1 }}>{eyebrow}</motion.p>
          ) : null}
          <h1 className={styles.h1}>
            <span className={styles.line}>{words(headline, 0.2)}</span>
            {accent ? <span className={[styles.line, styles.accent].join(' ')}>{words(accent, 0.45)}</span> : null}
          </h1>
          <motion.div className={styles.after} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.9, ease: EASE, delay: 0.9 }}>
            {sub ? <p className={styles.sub}>{sub}</p> : null}
            <div className={styles.ctas}>
              {primaryLabel ? <a className={styles.primary} href={primaryHref}>{primaryLabel}<Icon name="arrow" size={16} /></a> : null}
              {secondaryLabel ? <a className={styles.secondary} href={secondaryHref}>{secondaryLabel}</a> : null}
            </div>
            {trustList.length ? (
              <ul className={styles.trust}>
                {trustList.map((t, i) => <li key={i}>{t}</li>)}
              </ul>
            ) : null}
          </motion.div>
        </div>

        {list.length > 1 ? (
          <div className={styles.bar}>
            {list.map((s: any, i: number) => (
              <button key={i} type="button" className={[styles.tab, i === active ? styles.tabOn : ''].join(' ')} onClick={() => setActive(i)} aria-pressed={i === active}>
                <span className={styles.track}><span key={i === active ? 'on' + active : 'off'} className={styles.fill} /></span>
                <span className={styles.tabText}>{s.caption || s.alt}</span>
              </button>
            ))}
          </div>
        ) : null}
      </div>
    </section>
  );
}
