import React, { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image, { mediaUrl } from '@siteui/image';
import Icon from '@siteui/icon';
import styles from './styles.module.css';

function paras(t: any): string[] {
  return String(t || '').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}
function ok(x: any) {
  return x && x.src;
}

function Compare({ pair, beforeLabel, afterLabel, sliderLabel }: any) {
  const [pos, setPos] = useState(50);
  useEffect(() => setPos(50), [pair]);
  return (
    <div className={styles.compare} style={{ ['--pos' as any]: pos + '%' }}>
      <Image src={pair.after.src} alt={pair.afterAlt} className={styles.cImg} />
      <div className={styles.cBefore} aria-hidden="true">
        <Image src={pair.before.src} alt="" className={styles.cImg} />
      </div>
      <span className={[styles.cTag, styles.cTagL].join(' ')}>{beforeLabel}</span>
      <span className={[styles.cTag, styles.cTagR].join(' ')}>{afterLabel}</span>
      <span className={styles.cLine} aria-hidden="true">
        <span className={styles.cKnob}>
          <span className={styles.rot}><Icon name="chevron" size={16} /></span>
          <Icon name="chevron" size={16} />
        </span>
      </span>
      <input
        className={styles.cRange}
        type="range"
        min={0}
        max={100}
        step={0.5}
        value={pos}
        onChange={(e) => setPos(Number(e.target.value))}
        aria-label={sliderLabel + ': ' + pair.beforeAlt + ' / ' + pair.afterAlt}
      />
    </div>
  );
}

export default function Refs({
  eyebrow, title, intro, allLabel, categories,
  compareEyebrow, compareTitle, compareText, compareLinkLabel, compareLinkHref, pairs, beforeLabel, afterLabel,
  photos, photosLabel, openLabel, closeLabel, prevLabel, nextLabel, sliderLabel,
}: any) {
  const cats: any[] = (Array.isArray(categories) ? categories : []).filter((c: any) => c && c.key);
  const pairList: any[] = (Array.isArray(pairs) ? pairs : []).filter((p: any) => p && ok(p.before) && ok(p.after));
  const list: any[] = (Array.isArray(photos) ? photos : []).filter((p: any) => p && p.image && ok(p.image));

  const projects: any[] = [];
  list.forEach((ph: any) => {
    const key = String(ph.project || '').trim();
    let pr = projects.find((x) => x.title === key && x.category === ph.category);
    if (!pr) {
      pr = { title: key, category: ph.category, images: [] };
      projects.push(pr);
    }
    pr.images.push(ph);
  });

  const [cat, setCat] = useState('all');
  const [pi, setPi] = useState(0);
  const [box, setBox] = useState<{ p: number; i: number } | null>(null);
  const shown = projects.map((p, idx) => ({ p, idx })).filter((x) => cat === 'all' || x.p.category === cat);
  const imgs = box ? projects[box.p].images : [];
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
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = prev;
    };
  }, [box, close, step]);

  const catLabel = (k: string) => (cats.find((c: any) => c.key === k) || {}).label || '';
  const count = (k: string) => (k === 'all' ? list.length : list.filter((p: any) => p.category === k).length);
  const pair = pairList[Math.min(pi, Math.max(0, pairList.length - 1))];

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        {eyebrow || title || intro ? (
          <header className={styles.head}>
            {eyebrow ? <span className={styles.eyebrow}>{eyebrow}</span> : null}
            {title ? <h2 className={styles.title}>{title}</h2> : null}
            <div className={styles.intro}>{paras(intro).map((p, i) => <p key={i} className={styles.lead}>{p}</p>)}</div>
          </header>
        ) : null}

        {pair ? (
          <div className={styles.compareWrap}>
            <div className={styles.compareText}>
              {compareEyebrow ? <span className={styles.eyebrow}>{compareEyebrow}</span> : null}
              {compareTitle ? <h2 className={styles.h2}>{compareTitle}</h2> : null}
              {paras(compareText).map((p, i) => <p key={i} className={styles.p}>{p}</p>)}
              {compareLinkLabel && compareLinkHref ? <a className={styles.link} href={compareLinkHref}>{compareLinkLabel}<Icon name="arrow" size={16} /></a> : null}
              {pairList.length > 1 ? (
                <ol className={styles.pairList}>
                  {pairList.map((p: any, i: number) => (
                    <li key={i}>
                      <button type="button" className={[styles.pairBtn, i === pi ? styles.pairOn : ''].join(' ')} onClick={() => setPi(i)} aria-pressed={i === pi}>
                        <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
                        <span>{p.title}</span>
                      </button>
                    </li>
                  ))}
                </ol>
              ) : null}
            </div>
            <AnimatePresence mode="wait">
              <motion.div key={pi} className={styles.compareStage} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
                <Compare pair={pair} beforeLabel={beforeLabel} afterLabel={afterLabel} sliderLabel={sliderLabel} />
              </motion.div>
            </AnimatePresence>
          </div>
        ) : null}

        {projects.length ? (
          <div className={styles.gallery}>
            <div className={styles.filters} role="toolbar" aria-label={title}>
              {[{ key: 'all', label: allLabel }, ...cats].map((c: any) => (
                <button key={c.key} type="button" className={[styles.filter, cat === c.key ? styles.filterOn : ''].join(' ')} onClick={() => setCat(c.key)} aria-pressed={cat === c.key}>
                  {c.label}<sup className={styles.sup}>{count(c.key)}</sup>
                </button>
              ))}
            </div>
            <motion.div layout className={styles.grid}>
              <AnimatePresence>
                {shown.map(({ p, idx }, n) => {
                  const cover = p.images.find((x: any) => x.cover) || p.images[0];
                  return (
                    <motion.button
                      layout
                      key={p.category + p.title}
                      type="button"
                      className={[styles.tile, n % 6 === 0 ? styles.tileXL : n % 6 === 3 ? styles.tileTall : ''].join(' ')}
                      onClick={() => setBox({ p: idx, i: Math.max(0, p.images.indexOf(cover)) })}
                      aria-label={openLabel + ': ' + p.title}
                      initial={{ opacity: 0, y: 24 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                    >
                      <Image src={cover.image.src} alt={cover.alt} className={styles.tileImg} />
                      <span className={styles.tileShade} aria-hidden="true" />
                      <span className={styles.tileBody}>
                        <span className={styles.tileCat}>{catLabel(p.category)}</span>
                        <span className={styles.tileTitle}>{p.title}</span>
                        <span className={styles.tileMeta}>{p.images.length} {photosLabel}<Icon name="arrow" size={16} /></span>
                      </span>
                    </motion.button>
                  );
                })}
              </AnimatePresence>
            </motion.div>
          </div>
        ) : null}
      </div>

      <AnimatePresence>
        {box !== null && imgs[box.i] ? (
          <motion.div className={styles.lightbox} role="dialog" aria-modal="true" aria-label={projects[box.p].title} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={close}>
            <div className={styles.lbTop} onClick={(e) => e.stopPropagation()}>
              <span className={styles.lbCat}>{catLabel(projects[box.p].category)}</span>
              <span className={styles.lbTitle}>{projects[box.p].title}</span>
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
