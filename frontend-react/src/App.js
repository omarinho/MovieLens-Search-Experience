import React, { createContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import NoPage from "./pages/NoPage";
import { ConfigContext } from './contexts/ConfigContext';

const condigValueFromJson = require('./config.json');

export default function App() {
  return (
    <ConfigContext.Provider value={condigValueFromJson.API_SERVER_URL}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="*" element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>  
    </ConfigContext.Provider>
  );
}
