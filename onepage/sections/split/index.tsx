import React, { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image, { mediaUrl } from '@siteui/image';
import Icon from '@siteui/icon';
import Button from '@siteui/button';
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
function valid(list: any): any[] {
  return (Array.isArray(list) ? list : []).filter((x: any) => x && x.image && x.image.src);
}

export default function Split({ blocks, headingMode, projectsEyebrow, projectsTitle, photos, photosLabel, openLabel, closeLabel, prevLabel, nextLabel }: any) {
  const rows: any[] = Array.isArray(blocks) ? blocks : [];
  const cards: any[] = [];
  valid(photos).forEach((ph: any) => {
    const key = String(ph.project || '').trim();
    let card = cards.find((c) => c.title === key);
    if (!card) {
      card = { title: key, images: [] };
      cards.push(card);
    }
    card.images.push(ph);
  });
  const [box, setBox] = useState<{ p: number; i: number } | null>(null);
  const imgs = box ? valid(cards[box.p].images) : [];
  const close = useCallback(() => setBox(null), []);
  const step = useCallback((d: number) => setBox((b) => (b === null ? b : { p: b.p, i: (b.i + d + imgs.length) % imgs.length })), [imgs.length]);

  useEffect(() => {
    if (box === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    };
    window.addEventListener('keydown', onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [box, close, step]);

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        {rows.map((b: any, i: number) => (
          <div key={i} className={[styles.row, i % 2 === 1 ? styles.flip : ''].join(' ')}>
            <div className={styles.text}>
              {b.title ? (i === 0 && headingMode === 'h1first' ? <h1 className={styles.h1}>{b.title}</h1> : <h2 className={styles.h2}>{b.title}</h2>) : null}
              {paras(b.text).map((p, k) => <p key={k} className={i === 0 && k === 0 && headingMode === 'h1first' ? styles.lead : styles.p}>{rich(p)}</p>)}
              {lines(b.bullets).length ? (
                <ul className={styles.list}>
                  {lines(b.bullets).map((li, k) => <li key={k} className={styles.li}>{li}</li>)}
                </ul>
              ) : null}
              {paras(b.textAfter).map((p, k) => <p key={'a' + k} className={styles.p}>{rich(p)}</p>)}
              {b.linkLabel && b.linkHref ? <div className={styles.more}><Button href={b.linkHref} variant="link" size="md" arrow>{b.linkLabel}</Button></div> : null}
            </div>
            {b.linkHref ? (
              <a className={[styles.media, styles.mediaLink].join(' ')} href={b.linkHref} tabIndex={-1} aria-hidden="true">
                {b.image && b.image.src ? <Image src={b.image.src} alt="" className={styles.img} /> : null}
              </a>
            ) : (
              <div className={styles.media}>
                {b.image && b.image.src ? <Image src={b.image.src} alt={b.imageAlt} className={styles.img} /> : null}
              </div>
            )}
          </div>
        ))}

        {cards.length ? (
          <div className={styles.projects}>
            <div className={styles.projectsHead}>
              {projectsEyebrow ? <span className={styles.eyebrow}>{projectsEyebrow}</span> : null}
              {projectsTitle ? <h2 className={styles.projectsTitle}>{projectsTitle}</h2> : null}
            </div>
            <div className={styles.cards}>
              {cards.map((p: any, k: number) => {
                const list = valid(p.images);
                const cover = list.find((x: any) => x.cover) || list[0];
                return (
                  <button type="button" key={k} className={[styles.card, cards.length % 2 === 1 && k === 0 ? styles.wide : ''].join(' ')} onClick={() => setBox({ p: k, i: 0 })} aria-label={openLabel + ': ' + p.title}>
                    <span className={styles.cardMedia}>
                      <Image src={cover.image.src} alt={cover.alt} className={styles.img} />
                    </span>
                    <span className={styles.cardBody}>
                      <span className={styles.cardTitle}>{p.title}</span>
                      <span className={styles.cardMeta}>{list.length} {photosLabel}<Icon name="arrow" size={16} /></span>
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        ) : null}
      </div>

      <AnimatePresence>
        {box !== null && imgs[box.i] ? (
          <motion.div className={styles.lightbox} role="dialog" aria-modal="true" aria-label={cards[box.p].title} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={close}>
            <div className={styles.lbTop} onClick={(e) => e.stopPropagation()}>
              <span className={styles.lbTitle}>{cards[box.p].title}</span>
              <span className={styles.lbCount}>{box.i + 1} / {imgs.length}</span>
              <button type="button" className={styles.lbBtn} aria-label={closeLabel} onClick={close}><Icon name="close" size={24} /></button>
            </div>
            <div className={styles.lbStage}>
              <button type="button" className={[styles.lbBtn, styles.lbSide].join(' ')} aria-label={prevLabel} onClick={(e) => { e.stopPropagation(); step(-1); }}>
                <span className={styles.rot}><Icon name="chevron" size={26} /></span>
              </button>
              <motion.img key={box.i} className={styles.lbImg} src={mediaUrl(imgs[box.i].image.src, 'xlg')} alt={imgs[box.i].alt} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.3 }} onClick={(e) => e.stopPropagation()} />
              <button type="button" className={[styles.lbBtn, styles.lbSide].join(' ')} aria-label={nextLabel} onClick={(e) => { e.stopPropagation(); step(1); }}><Icon name="chevron" size={26} /></button>
            </div>
            {imgs.length > 1 ? (
              <div className={styles.thumbs} onClick={(e) => e.stopPropagation()}>
                {imgs.map((it: any, k: number) => (
                  <button type="button" key={k} className={[styles.thumb, k === box.i ? styles.thumbOn : ''].join(' ')} onClick={() => setBox({ p: box.p, i: k })} aria-label={openLabel + ' ' + (k + 1)}>
                    <img src={mediaUrl(it.image.src, 'sm')} alt="" loading="lazy" />
                  </button>
                ))}
              </div>
            ) : null}
          </motion.div>
        ) : null}
      </AnimatePresence>
    </section>
  );
}
