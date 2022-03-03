import React from 'react';
import Header from './Header';
import Footer from './Footer';
import { Outlet } from "react-router-dom";
import { LayoutWrap } from './styles/styled-layout';

const Layout = () => {
    return (
        <>
            <Header />
            <LayoutWrap>
                <Outlet /> 
            </LayoutWrap>
            <Footer />
        </>
    );
};

export default Layout;