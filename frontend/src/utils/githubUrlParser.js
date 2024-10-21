/**
 * Extracts the repository name from a GitHub URL.
 * @param {string} url - The GitHub URL.
 * @returns {string|null} The repository name or null if not found.
 */
export function getRepoNameFromUrl(url) {
  try {
    const parsedUrl = new URL(url);
    const pathParts = parsedUrl.pathname.split('/').filter(Boolean);
    
    // Check if the URL is in the correct format
    if (parsedUrl.hostname === 'github.com' && pathParts.length >= 2) {
      return pathParts[1];
    }
  } catch (error) {
    console.error('Error parsing GitHub URL:', error);
  }
  return null;
}

/**
 * Extracts the organization name from a GitHub URL.
 * @param {string} url - The GitHub URL.
 * @returns {string|null} The organization name or null if not found.
 */
export function getOrgNameFromUrl(url) {
  try {
    const parsedUrl = new URL(url);
    const pathParts = parsedUrl.pathname.split('/').filter(Boolean);
    
    // Check if the URL is in the correct format
    if (parsedUrl.hostname === 'github.com' && pathParts.length >= 1) {
      return pathParts[0];
    }
  } catch (error) {
    console.error('Error parsing GitHub URL:', error);
  }
  return null;
}
