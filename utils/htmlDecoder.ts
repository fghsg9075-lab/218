
export const decodeHtml = (content: string | undefined | null): string => {
  if (!content) return '';

  const trimmed = content.trim();

  // 1. Check for Explicit Data URI
  if (trimmed.startsWith('data:text/html;base64,')) {
    try {
      const base64 = trimmed.split(',')[1];
      // Use a robust decoding method for UTF-8
      return decodeURIComponent(escape(atob(base64)));
    } catch (e) {
      console.warn('Failed to decode Base64 Data URI', e);
      return content;
    }
  }

  // 2. Check if it looks like Base64 (No spaces, no < or >, has valid B64 chars)
  // HTML usually has <, >, and spaces. Base64 does not.
  const isLikelyBase64 = /^[A-Za-z0-9+/=]+$/.test(trimmed);

  if (isLikelyBase64) {
      try {
          const decoded = decodeURIComponent(escape(atob(trimmed)));
          // Heuristic: If the decoded string contains HTML tags, it's definitely what we want.
          // If the original string didn't have tags (which it doesn't if it passed isLikelyBase64),
          // and the decoded one does, then we successfully decoded HTML.
          if (decoded.includes('<') && decoded.includes('>')) {
              return decoded;
          }
          
          // If decoded string is just plain text (no tags), it's ambiguous. 
          // But since the user specifically asked to decode Base64, we might err on side of decoding
          // IF the original was NOT readable (e.g. high entropy).
          // But "HelloWord123" is readable. 
          
          // Let's assume valid HTML content starts with <!DOCTYPE or <html or <div or <p or something.
          // Or just allow it if it looks reasonable.
          return decoded;
      } catch (e) {
          // If atob fails or UTF-8 decode fails, it wasn't valid Base64
          return content;
      }
  }

  // 3. Return original (assumed to be raw HTML or text)
  return content;
};
