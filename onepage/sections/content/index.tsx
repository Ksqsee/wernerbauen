import React, { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image, { mediaUrl } from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

function paras(t: any): string[] {
  return String(t || '').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}
function lines(t: any): string[] {
  return String(t || '').split(/\n/).map((p) => p.trim()).filter(Boolean);
}
function rich(p: string) {
  const parts = p.split(/\*\*(.+?)\*\*/g);
  return parts.map((s, i) => (i % 2 === 1 ? <strong key={i}>{s}</strong> : <React.Fragment key={i}>{s}</React.Fragment>));
}

export default function Content({ blocks, images, closeLabel, prevLabel, nextLabel, openLabel }: any) {
  const list: any[] = Array.isArray(blocks) ? blocks : [];
  const imgs: any[] = (Array.isArray(images) ? images : []).filter((x: any) => x && x.image && x.image.src);
  const [active, setActive] = useState<number | null>(null);
  const close = useCallback(() => setActive(null), []);
  const prev = useCallback(() => setActive((a) => (a === null ? a : (a - 1 + imgs.length) % imgs.length)), [imgs.length]);
  const next = useCallback(() => setActive((a) => (a === null ? a : (a + 1) % imgs.length)), [imgs.length]);

  useEffect(() => {
    if (active === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') prev();
      if (e.key === 'ArrowRight') next();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [active, close, prev, next]);

  return (
    <section className={styles.section}>
      <div className={[styles.container, imgs.length ? styles.withGallery : ''].join(' ')}>
        <div className={styles.text}>
          {list.map((b: any, i: number) => (
            <div key={i} className={styles.block}>
              {b.title ? (i === 0 ? <h1 className={styles.h1}>{b.title}</h1> : <h2 className={styles.h2}>{b.title}</h2>) : null}
              {paras(b.text).map((p, k) => <p key={k} className={styles.p}>{rich(p)}</p>)}
              {lines(b.bullets).length ? (
                <ul className={styles.list}>
                  {lines(b.bullets).map((li, k) => <li key={k} className={styles.li}>{li}</li>)}
                </ul>
              ) : null}
              {paras(b.textAfter).map((p, k) => <p key={'a' + k} className={styles.p}>{rich(p)}</p>)}
            </div>
          ))}
        </div>
        {imgs.length ? (
          <div className={styles.grid}>
            {imgs.map((it: any, i: number) => (
              <button type="button" key={i} className={styles.tile} onClick={() => setActive(i)} aria-label={openLabel + ' ' + (i + 1)}>
                <Image src={it.image.src} alt={it.alt} className={styles.img} />
                <span className={styles.zoom}><Icon name="plus" size={18} /></span>
              </button>
            ))}
          </div>
        ) : null}
      </div>

      <AnimatePresence>
        {active !== null && imgs[active] ? (
          <motion.div className={styles.lightbox} role="dialog" aria-modal="true" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={close}>
            <button type="button" className={[styles.lbBtn, styles.lbClose].join(' ')} aria-label={closeLabel} onClick={close}><Icon name="close" size={26} /></button>
            <button type="button" className={[styles.lbBtn, styles.lbPrev].join(' ')} aria-label={prevLabel} onClick={(e) => { e.stopPropagation(); prev(); }}>
              <span className={styles.flip}><Icon name="chevron" size={28} /></span>
            </button>
            <motion.img key={active} className={styles.lbImg} src={mediaUrl(imgs[active].image.src, 'xlg')} alt={imgs[active].alt} initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.3 }} onClick={(e) => e.stopPropagation()} />
            <button type="button" className={[styles.lbBtn, styles.lbNext].join(' ')} aria-label={nextLabel} onClick={(e) => { e.stopPropagation(); next(); }}><Icon name="chevron" size={28} /></button>
            <span className={styles.counter}>{active + 1} / {imgs.length}</span>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </section>
  );
}
