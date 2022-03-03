import React from 'react';
import { Link } from 'react-router-dom'
import { FooterBar } from './styles/styled-footer';
import './styles/styles.css';

const Footer = () => {
    return (
        <FooterBar>
            Developed by&nbsp;
            <a className="footerLink" target="_blank" href="https://OmarYesidMarino.com">Omar Yesid Mari&ntilde;o</a>
        </FooterBar>
    );
};

export default Footer;