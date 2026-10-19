import React, { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image, { mediaUrl } from '@siteui/image';
import Title from '@siteui/title';
import { Eyebrow } from '@siteui/text';
import Button from '@siteui/button';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

export default function Gallery({ eyebrow, title, images, initialCount, stepCount, moreLabel, closeLabel, prevLabel, nextLabel, openLabel, tone }: any) {
  const list: any[] = (Array.isArray(images) ? images : []).filter((x: any) => x && x.image && x.image.src);
  const [visible, setVisible] = useState(Number(initialCount));
  const [active, setActive] = useState<number | null>(null);

  const close = useCallback(() => setActive(null), []);
  const prev = useCallback(() => setActive((a) => (a === null ? a : (a - 1 + list.length) % list.length)), [list.length]);
  const next = useCallback(() => setActive((a) => (a === null ? a : (a + 1) % list.length)), [list.length]);

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

  const shown = list.slice(0, visible);
  return (
    <section className={[styles.section, styles['tone_' + tone]].join(' ')}>
      <div className={styles.container}>
        {eyebrow || title ? (
          <div className={styles.head}>
            {eyebrow ? <Eyebrow tone={tone === 'dark' ? 'light' : 'dark'}>{eyebrow}</Eyebrow> : null}
            {title ? <Title as="h2" size="lg" tone={tone === 'dark' ? 'light' : 'dark'}>{title}</Title> : null}
          </div>
        ) : null}
        <div className={styles.grid}>
          {shown.map((it: any, i: number) => (
            <motion.button
              type="button"
              key={i}
              className={[styles.tile, i % 7 === 0 ? styles.wide : ''].join(' ')}
              onClick={() => setActive(i)}
              aria-label={openLabel + ': ' + (it.alt || String(i + 1))}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.1 }}
              transition={{ duration: 0.6, delay: (i % 3) * 0.06 }}
            >
              <Image src={it.image.src} alt={it.alt} className={styles.img} />
              <span className={styles.zoom}><Icon name="plus" size={22} /></span>
            </motion.button>
          ))}
        </div>
        {visible < list.length ? (
          <div className={styles.more}>
            <Button variant={tone === 'dark' ? 'outlineLight' : 'outline'} size="md" onClick={() => setVisible(visible + Number(stepCount))}>
              {moreLabel} ({list.length - visible})
            </Button>
          </div>
        ) : null}
      </div>

      <AnimatePresence>
        {active !== null && list[active] ? (
          <motion.div
            className={styles.lightbox}
            role="dialog"
            aria-modal="true"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={close}
          >
            <button type="button" className={[styles.lbBtn, styles.lbClose].join(' ')} aria-label={closeLabel} onClick={close}>
              <Icon name="close" size={26} />
            </button>
            <button type="button" className={[styles.lbBtn, styles.lbPrev].join(' ')} aria-label={prevLabel} onClick={(e) => { e.stopPropagation(); prev(); }}>
              <span className={styles.flip}><Icon name="chevron" size={28} /></span>
            </button>
            <motion.img
              key={active}
              className={styles.lbImg}
              src={mediaUrl(list[active].image.src, 'xlg')}
              alt={list[active].alt}
              initial={{ opacity: 0, scale: 0.97 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              onClick={(e) => e.stopPropagation()}
            />
            <button type="button" className={[styles.lbBtn, styles.lbNext].join(' ')} aria-label={nextLabel} onClick={(e) => { e.stopPropagation(); next(); }}>
              <Icon name="chevron" size={28} />
            </button>
            <span className={styles.counter}>{active + 1} / {list.length}</span>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </section>
  );
}
