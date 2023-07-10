import React from 'react';
import AdminNav from './components/navbar';
import Home from './pages/Home';
import useTheme from './hooks/useTheme';

function App() {
  const {theme, toggleTheme} = useTheme();

  return (
    <div>
      <AdminNav />
      <Home />
      <button onClick={toggleTheme}>Toggle '{theme}' Theme</button>
    </div>
  );
}

export default App;