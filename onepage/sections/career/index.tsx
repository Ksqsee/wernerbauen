import React, { useState } from 'react';
import { crm } from 'onepage-kit';
import Text from '@siteui/text';
import Button from '@siteui/button';
import Icon from '@siteui/icon';
import FormField from '@siteui/form-field';
import FileUpload from '@siteui/file-upload';
import VoiceNote from './voice';
import styles from './styles.module.css';

const EMPTY = { firstName: '', lastName: '', email: '', phone: '', position: '', message: '' };

function lines(t: any): string[] {
  return String(t || '').split(/\n/).map((p) => p.trim()).filter(Boolean);
}
function paras(t: any): string[] {
  return String(t || '').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}

export default function Career({
  title, intro, benefitsTitle, benefits, initiativeTitle, initiativeText, applyLabel,
  formAnchor, formTitle, formIntro, firstNameLabel, lastNameLabel, emailLabel, phoneLabel, positionLabel, messageLabel,
  attachLabel, attachHint, attachButton, attachRemove, attachTooLarge, attachAccept, attachMaxFiles, attachMaxMb,
  consentPre, privacyLabel, privacyHref, consentPost, requiredNote, submitLabel, sendingLabel, successText, errorText, requiredError, emailError,
  formId, langTitle, langLinks,
  jobEyebrow, jobTitle, jobMeta, jobHook, jobIntro, jobMoreLabel, jobLessLabel,
  jobTasksTitle, jobTasks, jobProfileTitle, jobProfile, jobOfferTitle, jobOffer, jobNote,
  jobContactTitle, jobContactName, jobContactPhone, jobContactPhoneHref, jobContactEmail, jobApplyLabel,
  voiceLabel, voiceHint, voiceRecord, voiceStop, voiceRecording, voiceDelete, voiceDenied, voiceFileHint,
}: any) {
  const benefitList: any[] = Array.isArray(benefits) ? benefits : [];
  const langList: any[] = Array.isArray(langLinks) ? langLinks : [];
  const [data, setData] = useState<any>(EMPTY);
  const [files, setFiles] = useState<File[]>([]);
  const [voice, setVoice] = useState<File | null>(null);
  const [jobOpen, setJobOpen] = useState(false);
  const [errors, setErrors] = useState<any>({});
  const [status, setStatus] = useState<'idle' | 'sending' | 'ok' | 'error'>('idle');

  const set = (k: string) => (v: string) => setData({ ...data, [k]: v });
  const toForm = (pos?: string) => {
    if (pos) setData((d: any) => ({ ...d, position: pos }));
    const el = typeof document !== 'undefined' ? document.getElementById(formAnchor) : null;
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const validate = () => {
    const e: any = {};
    ['firstName', 'lastName', 'email'].forEach((k) => { if (!String(data[k]).trim()) e[k] = requiredError; });
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) e.email = emailError;
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (!validate()) return;
    setStatus('sending');
    try {
      const attachments = [];
      for (const f of files) attachments.push(await crm.uploadFormFile(f));
      if (voice) attachments.push(await crm.uploadFormFile(voice));
      await crm.submitForm({ formId, data: { ...data, attachments } });
      setStatus('ok');
      setData(EMPTY);
      setFiles([]);
      setVoice(null);
    } catch (err) {
      setStatus('error');
    }
  };

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.top}>
          <div className={styles.intro}>
            {title ? <h1 className={styles.h1}>{title}</h1> : null}
            {langList.filter((l: any) => !l.current).length ? (
              <nav className={styles.langs} aria-label={langTitle}>
                <span className={styles.langsTitle}>{langTitle}</span>
                {langList.filter((l: any) => !l.current).map((l: any, i: number) => (
                  <a key={i} className={styles.langLink} href={l.href} hrefLang={l.code} lang={l.code}>{l.label}</a>
                ))}
              </nav>
            ) : null}
            {paras(intro).map((p, i) => <p key={i} className={i === 0 ? styles.lead : styles.p}>{p}</p>)}
            <div className={styles.cta}>
              <Button href={'#' + formAnchor} variant="primary" size="md" arrow onClick={(e) => { e.preventDefault(); toForm(); }}>{applyLabel}</Button>
            </div>
          </div>
          <div className={styles.benefitsCol}>
            <h2 className={styles.h2}>{benefitsTitle}</h2>
            <ol className={styles.benefits}>
              {benefitList.map((b: any, i: number) => (
                <li key={i} className={styles.benefit}>
                  <span className={styles.num} aria-hidden="true">{String(i + 1).padStart(2, '0')}</span>
                  <span>{b.text}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>

        {jobTitle ? (
          <article className={styles.job}>
            <div className={styles.jobHead}>
              {jobEyebrow ? <span className={styles.eyebrow}>{jobEyebrow}</span> : null}
              <h2 className={styles.jobTitle}>{jobTitle}</h2>
              {jobMeta ? <p className={styles.jobMeta}>{jobMeta}</p> : null}
            </div>
            <div className={styles.jobBody}>
              {jobHook ? <p className={styles.jobHook}>{jobHook}</p> : null}
              {paras(jobIntro).map((p, i) => <p key={i} className={i === 0 ? styles.lead : styles.p}>{p}</p>)}
              <div className={styles.jobActions}>
                <Button href={'#' + formAnchor} variant="primary" size="md" arrow onClick={(e) => { e.preventDefault(); toForm(jobTitle); }}>{jobApplyLabel}</Button>
                <button type="button" className={styles.more} aria-expanded={jobOpen} aria-controls="job-details" onClick={() => setJobOpen(!jobOpen)}>
                  {jobOpen ? jobLessLabel : jobMoreLabel}
                  <span className={[styles.caret, jobOpen ? styles.caretUp : ''].join(' ')}><Icon name="chevron" size={14} /></span>
                </button>
              </div>
            </div>
            {jobOpen ? (
              <div id="job-details" className={styles.jobDetails}>
                {[[jobTasksTitle, jobTasks], [jobProfileTitle, jobProfile], [jobOfferTitle, jobOffer]].map(([t, l]: any, k: number) => (
                  <div key={k} className={styles.jobCol}>
                    <h3 className={styles.jobColTitle}>{t}</h3>
                    <ul className={styles.list}>{lines(l).map((li, n) => <li key={n} className={styles.li}>{li}</li>)}</ul>
                  </div>
                ))}
                {jobNote ? <p className={styles.jobNote}>{jobNote}</p> : null}
                {jobContactName ? (
                  <div className={styles.jobContact}>
                    <span className={styles.eyebrow}>{jobContactTitle}</span>
                    <strong className={styles.jobContactName}>{jobContactName}</strong>
                    <span className={styles.jobContactLinks}>
                      {jobContactPhone ? <a href={jobContactPhoneHref}>{jobContactPhone}</a> : null}
                      {jobContactEmail ? <a href={'mailto:' + jobContactEmail}>{jobContactEmail}</a> : null}
                    </span>
                  </div>
                ) : null}
              </div>
            ) : null}
          </article>
        ) : null}

        <div className={styles.initiative}>
          <h2 className={styles.initiativeTitle}>{initiativeTitle}</h2>
          <div className={styles.initiativeBody}>
            {paras(initiativeText).map((p, i) => <p key={i} className={i === 0 ? styles.lead : styles.p}>{p}</p>)}
            <div className={styles.cta}>
              <Button href={'#' + formAnchor} variant="primary" size="md" arrow onClick={(e) => { e.preventDefault(); toForm(); }}>{applyLabel}</Button>
            </div>
          </div>
        </div>

        <div id={formAnchor} className={styles.formWrap}>
          <div className={styles.col}>
            <h2 className={styles.sectionTitle}>{formTitle}</h2>
            {paras(formIntro).map((p, i) => <p key={i} className={styles.p}>{p}</p>)}
          </div>
          {status === 'ok' ? (
            <div className={styles.success} role="status">
              <span className={styles.okIcon}><Icon name="check" size={22} /></span>
              <Text size="md">{successText}</Text>
            </div>
          ) : (
            <form className={styles.form} onSubmit={submit} noValidate>
              <div className={styles.row}>
                <FormField id="firstName" label={firstNameLabel} value={data.firstName} onChange={set('firstName')} required error={errors.firstName} autoComplete="given-name" />
                <FormField id="lastName" label={lastNameLabel} value={data.lastName} onChange={set('lastName')} required error={errors.lastName} autoComplete="family-name" />
              </div>
              <div className={styles.row}>
                <FormField id="email" label={emailLabel} type="email" value={data.email} onChange={set('email')} required error={errors.email} autoComplete="email" />
                <FormField id="phone" label={phoneLabel} type="tel" value={data.phone} onChange={set('phone')} autoComplete="tel" />
              </div>
              <FormField id="position" label={positionLabel} value={data.position} onChange={set('position')} />
              <FormField id="message" label={messageLabel} value={data.message} onChange={set('message')} multiline />
              <VoiceNote value={voice} onChange={setVoice} label={voiceLabel} hint={voiceHint} recordLabel={voiceRecord} stopLabel={voiceStop} recordingLabel={voiceRecording} deleteLabel={voiceDelete} deniedText={voiceDenied} fileHint={voiceFileHint} filePrefix="bewerbung-sprachnachricht" />
              <FileUpload id="attachments" label={attachLabel} hint={attachHint} buttonLabel={attachButton} removeLabel={attachRemove} tooLargeText={attachTooLarge} accept={attachAccept} maxFiles={Number(attachMaxFiles)} maxSizeMb={Number(attachMaxMb)} files={files} onChange={setFiles} />
              <p className={styles.note}>{consentPre} <a className={styles.red} href={privacyHref}>{privacyLabel}</a> {consentPost}</p>
              <p className={styles.note}>{requiredNote}</p>
              {status === 'error' ? <p className={[styles.note, styles.red].join(' ')}>{errorText}</p> : null}
              <div>
                <Button type="submit" variant="primary" size="md" arrow disabled={status === 'sending'}>
                  {status === 'sending' ? sendingLabel : submitLabel}
                </Button>
              </div>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
