import React from 'react';
import { motion } from 'framer-motion';
import styles from './styles.module.css';

const EASE = [0.22, 1, 0.36, 1];

export default function Steps({ eyebrow, title, intro, steps, benefits }: any) {
  const list: any[] = Array.isArray(steps) ? steps : [];
  const perks: any[] = Array.isArray(benefits) ? benefits : [];
  const view = { once: true, margin: '-120px' };
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

        <div className={styles.timeline}>
          <motion.span className={styles.line} aria-hidden="true" initial={{ scaleX: 0 }} whileInView={{ scaleX: 1 }} viewport={view} transition={{ duration: 1.6, ease: EASE }} />
          <ol className={styles.steps}>
            {list.map((s: any, i: number) => {
              const you = i === 0;
              return (
                <motion.li
                  key={i}
                  className={styles.step}
                  initial={{ opacity: 0, y: 24 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={view}
                  transition={{ duration: 0.8, ease: EASE, delay: 0.25 + i * 0.18 }}
                >
                  <span className={[styles.marker, you ? styles.markerYou : ''].join(' ')} aria-hidden="true" />
                  <p className={styles.meta}>
                    <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
                    {s.who ? <span className={[styles.who, you ? styles.whoYou : ''].join(' ')}>{s.who}</span> : null}
                  </p>
                  <h3 className={styles.stepTitle}>{s.title}</h3>
                  <p className={styles.stepText}>{s.text}</p>
                </motion.li>
              );
            })}
          </ol>
        </div>

        {perks.length ? (
          <ul className={styles.perks}>
            {perks.map((b: any, i: number) => (
              <li key={i} className={styles.perk}>
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
