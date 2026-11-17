import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from '@siteui/image';
import styles from './styles.module.css';

const EASE = [0.22, 1, 0.36, 1];

function rows(t: any): string[][] {
  return String(t || '').split('\n').map((l) => l.trim()).filter(Boolean).map((l) => l.split('|').map((x) => x.trim()));
}

export default function Process({ eyebrow, title, intro, steps, benefits, panelLabel, exampleLabel, seconds }: any) {
  const list: any[] = (Array.isArray(steps) ? steps : []).filter((s: any) => s && s.title);
  const perks: any[] = Array.isArray(benefits) ? benefits : [];
  const [active, setActive] = useState(0);
  const [paused, setPaused] = useState(false);
  const [still, setStill] = useState(false);
  const secs = Math.max(3, Number(seconds) || 6);

  useEffect(() => {
    setStill(!!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches));
  }, []);
  useEffect(() => {
    if (paused || still || list.length < 2) return;
    const t = window.setTimeout(() => setActive((a) => (a + 1) % list.length), secs * 1000);
    return () => window.clearTimeout(t);
  }, [active, paused, still, list.length, secs]);

  const s = list[active] || {};
  const photos = [s.photo1, s.photo2, s.photo3].filter((p: any) => p && p.src);
  const pad = (n: number) => String(n).padStart(2, '0');

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.head}>
          <div className={styles.headLeft}>
            {eyebrow ? <p className={styles.eyebrow}>{eyebrow}</p> : null}
            {title ? <h2 className={styles.title}>{title}</h2> : null}
          </div>
          {intro ? <p className={styles.intro}>{intro}</p> : null}
        </div>

        <div className={styles.grid} onMouseEnter={() => setPaused(true)} onMouseLeave={() => setPaused(false)}>
          <ol className={styles.steps}>
            {list.map((st: any, i: number) => {
              const on = i === active;
              return (
                <li key={i} className={[styles.step, on ? styles.stepOn : ''].join(' ')}>
                  <button type="button" className={styles.stepBtn} onClick={() => setActive(i)} aria-pressed={on}>
                    <span className={styles.stepMeta}>
                      <span className={styles.num}>{pad(i + 1)}</span>
                      {st.who ? <span className={[styles.who, i === 0 ? styles.whoYou : ''].join(' ')}>{st.who}</span> : null}
                    </span>
                    <span className={styles.stepTitle}>{st.title}</span>
                  </button>
                  <AnimatePresence initial={false}>
                    {on ? (
                      <motion.p className={styles.stepText} initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.45, ease: EASE }}>
                        {st.text}
                      </motion.p>
                    ) : null}
                  </AnimatePresence>
                  <span className={styles.track} aria-hidden="true">
                    {on ? <span key={active + (paused ? 'p' : 'r')} className={[styles.fill, paused || still ? styles.fillFull : ''].join(' ')} style={{ animationDuration: secs + 's' }} /> : null}
                  </span>
                </li>
              );
            })}
          </ol>

          <div className={styles.window} aria-live="polite">
            <div className={styles.bar}>
              <span className={styles.live} aria-hidden="true" />
              <span className={styles.barLabel}>{panelLabel}</span>
              <span className={styles.barStep}>{pad(active + 1)} / {pad(list.length)}</span>
              {exampleLabel ? <span className={styles.example}>{exampleLabel}</span> : null}
            </div>
            <AnimatePresence mode="wait">
              <motion.div key={active} className={styles.body} initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.45, ease: EASE }}>
                <div className={styles.bodyHead}>
                  <span className={styles.panelTitle}>{s.panelTitle}</span>
                  {s.status ? <span className={styles.status}><span className={styles.statusDot} />{s.status}</span> : null}
                </div>

                {rows(s.panelRows).length ? (
                  <dl className={styles.rows}>
                    {rows(s.panelRows).map((r, i) => (
                      <motion.div key={i} className={styles.row} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.4, delay: 0.15 + i * 0.08 }}>
                        <dt>{r[0]}</dt>
                        <dd>{r[1] || ''}</dd>
                      </motion.div>
                    ))}
                  </dl>
                ) : null}

                {rows(s.panelDays).length ? (
                  <div className={styles.days}>
                    {rows(s.panelDays).map((d, i) => (
                      <motion.div key={i} className={[styles.day, d[2] ? styles.dayOn : ''].join(' ')} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 + i * 0.06 }}>
                        <span className={styles.dayName}>{d[0]}</span>
                        <span className={styles.dayNum}>{d[1]}</span>
                        {d[2] ? <span className={styles.slot}>{d[2]}</span> : null}
                      </motion.div>
                    ))}
                  </div>
                ) : null}

                {rows(s.panelBars).length ? (
                  <div className={styles.bars}>
                    {rows(s.panelBars).map((b, i) => {
                      const v = Math.max(0, Math.min(100, Number(b[1]) || 0));
                      return (
                        <div key={i} className={styles.barRow}>
                          <span className={styles.barName}>{b[0]}</span>
                          <span className={styles.barTrack}>
                            <motion.span className={styles.barFill} initial={{ width: 0 }} animate={{ width: v + '%' }} transition={{ duration: 1.1, ease: EASE, delay: 0.2 + i * 0.12 }} />
                          </span>
                          <span className={styles.barVal}>{v}%</span>
                        </div>
                      );
                    })}
                  </div>
                ) : null}

                {photos.length ? (
                  <div className={styles.photos}>
                    {photos.map((p: any, i: number) => (
                      <motion.figure key={i} className={styles.photo} initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5, delay: 0.25 + i * 0.1 }}>
                        <Image src={p.src} alt="" className={styles.photoImg} />
                        {[s.photo1Label, s.photo2Label, s.photo3Label][[s.photo1, s.photo2, s.photo3].indexOf(p)] ? (
                          <figcaption>{[s.photo1Label, s.photo2Label, s.photo3Label][[s.photo1, s.photo2, s.photo3].indexOf(p)]}</figcaption>
                        ) : null}
                      </motion.figure>
                    ))}
                  </div>
                ) : null}

                {s.footer ? <p className={styles.footer}><span className={styles.mono}>&gt;</span> {s.footer}</p> : null}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>

        {perks.length ? (
          <ul className={styles.perks}>
            {perks.map((b: any, i: number) => (
              <li key={i} className={styles.perk}>
                <span className={styles.perkNum}>{pad(i + 1)}</span>
                <p className={styles.perkTitle}>{b.title}</p>
                <p className={styles.perkText}>{b.text}</p>
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </section>
  );
}
