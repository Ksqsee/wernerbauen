import React from 'react';
import { mediaUrl } from '@siteui/image';
import styles from './styles.module.css';

export default function Banner({ image, imageAlt, height }: any) {
  const bg = image && image.src ? mediaUrl(image.src, 'xlg2x') : '';
  return (
    <section className={[styles.banner, styles['h_' + height]].join(' ')} role="img" aria-label={imageAlt} style={{ backgroundImage: bg ? 'url(' + bg + ')' : undefined }} />
  );
}
