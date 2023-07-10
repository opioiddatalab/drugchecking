import { useState, useEffect } from 'react';

// Custom hook to manage the site theme
function useTheme() {
  const [theme, setTheme] = useState('dark');

  // Apply the theme class to the document body
  useEffect(() => {
    document.body.className = `theme-${theme}`;
  }, [theme]);

  // Toggle the theme between light and dark
  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  return {
    theme,
    toggleTheme,
  };
}

export default useTheme;
