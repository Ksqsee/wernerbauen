import React from 'react';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Steps({ eyebrow, title, intro, steps, benefits }: any) {
  const list: any[] = Array.isArray(steps) ? steps : [];
  const perks: any[] = Array.isArray(benefits) ? benefits : [];
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.head}>
          {eyebrow ? <p className={styles.eyebrow}>{eyebrow}</p> : null}
          {title ? <h2 className={styles.title}>{title}</h2> : null}
          {intro ? <p className={styles.intro}>{intro}</p> : null}
        </div>
        <ol className={styles.steps}>
          {list.map((s: any, i: number) => (
            <li key={i} className={[styles.step, i === list.length - 1 ? styles.stepLast : ''].join(' ')}>
              <div className={styles.stepTop}>
                <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
                {s.who ? <span className={styles.who}>{s.who}</span> : null}
              </div>
              <h3 className={styles.stepTitle}>{s.title}</h3>
              <p className={styles.stepText}>{s.text}</p>
            </li>
          ))}
        </ol>
        {perks.length ? (
          <ul className={styles.perks}>
            {perks.map((b: any, i: number) => (
              <li key={i} className={styles.perk}>
                <span className={styles.check}><Icon name="check" size={14} /></span>
                <div>
                  <p className={styles.perkTitle}>{b.title}</p>
                  <p className={styles.perkText}>{b.text}</p>
                </div>
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </section>
  );
}
