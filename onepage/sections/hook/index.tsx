import React, { useEffect, useState } from 'react';
import Image from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Hook({ eyebrow, headline, accent, sub, primaryLabel, primaryHref, secondaryLabel, secondaryHref, slides, interval, links }: any) {
  const list: any[] = (Array.isArray(slides) ? slides : []).filter((s: any) => s && s.image && s.image.src);
  const items: any[] = Array.isArray(links) ? links : [];
  const [active, setActive] = useState(0);

  useEffect(() => {
    if (list.length < 2) return;
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;
    const t = window.setInterval(() => setActive((a) => (a + 1) % list.length), Math.max(3, Number(interval)) * 1000);
    return () => window.clearInterval(t);
  }, [list.length, interval]);

  return (
    <section className={styles.hook}>
      <div className={styles.media}>
        {list.map((s: any, i: number) => (
          <div key={i} className={[styles.slide, i === active ? styles.slideOn : ''].join(' ')} aria-hidden={i === active ? undefined : true}>
            <Image src={s.image.src} alt={s.alt} className={styles.img} />
          </div>
        ))}
        <div className={styles.shade} aria-hidden="true" />
        {list[active] && list[active].caption ? <p className={styles.caption}>{list[active].caption}</p> : null}
        {list.length > 1 ? (
          <div className={styles.dots}>
            {list.map((s: any, i: number) => (
              <button key={i} type="button" className={[styles.dot, i === active ? styles.dotOn : ''].join(' ')} aria-label={s.alt} aria-pressed={i === active} onClick={() => setActive(i)} />
            ))}
          </div>
        ) : null}
      </div>
      <div className={styles.content}>
        <div className={styles.copy}>
          {eyebrow ? <p className={styles.eyebrow}>{eyebrow}</p> : null}
          <h1 className={styles.h1}>
            {headline}
            {accent ? <span className={styles.accent}>{accent}</span> : null}
          </h1>
          {sub ? <p className={styles.sub}>{sub}</p> : null}
          <div className={styles.ctas}>
            {primaryLabel ? <a className={styles.primary} href={primaryHref}>{primaryLabel}<Icon name="arrow" size={16} /></a> : null}
            {secondaryLabel ? <a className={styles.secondary} href={secondaryHref}>{secondaryLabel}</a> : null}
          </div>
        </div>
        {items.length ? (
          <nav className={styles.links} aria-label={eyebrow}>
            {items.map((l: any, i: number) => (
              <a key={i} className={styles.link} href={l.href}>
                <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
                <span className={styles.linkLabel}>{l.label}</span>
                <Icon name="arrow" size={16} />
              </a>
            ))}
          </nav>
        ) : null}
      </div>
    </section>
  );
}
