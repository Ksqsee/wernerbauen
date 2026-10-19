import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { crm } from 'onepage-kit';
import Title from '@siteui/title';
import Text from '@siteui/text';
import Button from '@siteui/button';
import Icon from '@siteui/icon';
import FormField from '@siteui/form-field';
import styles from './styles.module.css';

const EMPTY = { firstName: '', lastName: '', company: '', phone: '', email: '', message: '' };

export default function Contact({
  infoTitle, companyLines, phoneLabel, phone, phoneHref, faxLabel, fax, emailLabel, email,
  formTitle, firstNameLabel, lastNameLabel, companyLabel, phoneFieldLabel, emailFieldLabel, messageLabel,
  consentText, privacyLabel, privacyHref, requiredNote, submitLabel, sendingLabel, successText, errorText, requiredError, emailError,
  formId,
}: any) {
  const [data, setData] = useState<any>(EMPTY);
  const [errors, setErrors] = useState<any>({});
  const [status, setStatus] = useState<'idle' | 'sending' | 'ok' | 'error'>('idle');
  const lines = String(companyLines).split(/\n/).filter((l) => l.trim());

  const set = (k: string) => (v: string) => setData({ ...data, [k]: v });

  const validate = () => {
    const e: any = {};
    ['firstName', 'lastName', 'email', 'message'].forEach((k) => { if (!String(data[k]).trim()) e[k] = requiredError; });
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) e.email = emailError;
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (!validate()) return;
    setStatus('sending');
    try {
      await crm.submitForm({ formId, data });
      setStatus('ok');
      setData(EMPTY);
    } catch (err) {
      setStatus('error');
    }
  };

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <motion.aside
          className={styles.info}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.2 }}
          transition={{ duration: 0.7 }}
        >
          <Title as="h2" size="md" tone="light">{infoTitle}</Title>
          <div className={styles.address}>
            <span className={styles.pin}><Icon name="pin" size={20} /></span>
            <div>
              {lines.map((l, i) => <Text key={i} size="md" tone={i === 0 ? 'light' : 'lightMuted'} className={i === 0 ? styles.company : ''}>{l}</Text>)}
            </div>
          </div>
          <div className={styles.channels}>
            <a className={styles.channel} href={phoneHref}>
              <span className={styles.chIcon}><Icon name="phone" size={18} /></span>
              <span><span className={styles.chLabel}>{phoneLabel}</span><span className={styles.chValue}>{phone}</span></span>
            </a>
            <div className={styles.channel}>
              <span className={styles.chIcon}><Icon name="fax" size={18} /></span>
              <span><span className={styles.chLabel}>{faxLabel}</span><span className={styles.chValue}>{fax}</span></span>
            </div>
            <a className={styles.channel} href={'mailto:' + email}>
              <span className={styles.chIcon}><Icon name="mail" size={18} /></span>
              <span><span className={styles.chLabel}>{emailLabel}</span><span className={styles.chValue}>{email}</span></span>
            </a>
          </div>
        </motion.aside>

        <motion.div
          className={styles.formWrap}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.2 }}
          transition={{ duration: 0.7, delay: 0.1 }}
        >
          <Title as="h2" size="md">{formTitle}</Title>
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
                <FormField id="company" label={companyLabel} value={data.company} onChange={set('company')} autoComplete="organization" />
                <FormField id="phone" label={phoneFieldLabel} type="tel" value={data.phone} onChange={set('phone')} autoComplete="tel" />
              </div>
              <FormField id="email" label={emailFieldLabel} type="email" value={data.email} onChange={set('email')} required error={errors.email} autoComplete="email" />
              <FormField id="message" label={messageLabel} value={data.message} onChange={set('message')} required multiline error={errors.message} />
              <Text size="sm" tone="muted">
                {consentText} <a className={styles.privacy} href={privacyHref}>{privacyLabel}</a>
              </Text>
              <Text size="sm" tone="muted">{requiredNote}</Text>
              {status === 'error' ? <Text size="sm" className={styles.err}>{errorText}</Text> : null}
              <div>
                <Button type="submit" variant="primary" size="lg" arrow disabled={status === 'sending'}>
                  {status === 'sending' ? sendingLabel : submitLabel}
                </Button>
              </div>
            </form>
          )}
        </motion.div>
      </div>
    </section>
  );
}
