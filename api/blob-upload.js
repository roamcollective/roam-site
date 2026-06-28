import { handleUpload } from '@vercel/blob/client';

// Generates short-lived tokens so the browser can upload reference files
// (images, STL, 3MF, STEP...) straight to Vercel Blob — bypassing the
// 4.5 MB serverless body limit. Requires a Blob store connected in Vercel
// (which auto-sets BLOB_READ_WRITE_TOKEN).

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const jsonResponse = await handleUpload({
      request: req,
      body: typeof req.body === 'string' ? JSON.parse(req.body) : req.body,
      onBeforeGenerateToken: async () => ({
        addRandomSuffix: true,
        maximumSizeInBytes: 50 * 1024 * 1024, // 50 MB
      }),
      onUploadCompleted: async () => {
        // Optional hook (won't fire on localhost). Left empty by design.
      },
    });

    return res.status(200).json(jsonResponse);
  } catch (err) {
    console.error('blob-upload error:', err);
    return res.status(400).json({ error: err?.message || 'Upload failed' });
  }
}
