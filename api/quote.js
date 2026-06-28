import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const esc = (s) =>
  String(s ?? '').replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const d = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};

    if (!d.name || !d.contact || !d.description) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const rows = [
      ['Name', d.name],
      ['Contact', d.contact],
      ['What they want printed', d.description],
      ['Size', d.size],
      ['Budget', d.budget],
      ['Timeline', d.timeline],
      ['Quantity', d.quantity],
      ['Reference link', d.referenceLink],
      ['Uploaded file', d.fileUrl],
    ].filter(([, v]) => v);

    const html =
      `<h2 style="font-family:sans-serif">New print request</h2>` +
      rows
        .map(
          ([k, v]) =>
            `<p style="font-family:sans-serif;margin:6px 0"><strong>${esc(k)}:</strong> ` +
            (String(v).startsWith('http')
              ? `<a href="${esc(v)}">${esc(v)}</a>`
              : esc(v)) +
            `</p>`
        )
        .join('');

    const params = {
      from: process.env.QUOTE_FROM_EMAIL,
      to: process.env.QUOTE_TO_EMAIL,
      subject: `New print request — ${d.name}`,
      html,
    };
    if (typeof d.contact === 'string' && d.contact.includes('@')) {
      params.replyTo = d.contact.trim();
    }

    const { error } = await resend.emails.send(params);
    if (error) {
      console.error('Resend error:', error);
      return res.status(502).json({ error: 'Email provider rejected the request' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('quote handler error:', err);
    return res.status(500).json({ error: 'Failed to send request' });
  }
}
