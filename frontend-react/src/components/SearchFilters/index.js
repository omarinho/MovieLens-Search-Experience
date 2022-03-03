import React, { useState, useContext } from 'react';
import { Wrap, FilterDiv } from './styles/styled-search-filters';

const SearchFilters = (props) => {

    const handleChange = (event, property) => {
        props.onUpdatedFilters(event.target.value, property);
    }
    
    return (
        <form>
            <Wrap>
                <FilterDiv>
                    <b>Filter by title:&nbsp;</b>
                    <input type="text" maxLength="255" value={props.filterValues.title} onChange={(e) => handleChange(e, 'title')} placeholder="Start Typing"/>
                </FilterDiv>
                <FilterDiv>
                    <b>Filter by genre:&nbsp;</b>
                    <select value={props.filterValues.genre} onChange={(e) => handleChange(e, 'genre')}>
                        <option value="">All</option>
                       {props.genres && props.genres.map( (elem) => <option key={elem.genre_id} value={elem.genre_id}>{elem.name}</option> )}
                    </select>                        
                </FilterDiv>
                <FilterDiv>
                    <b>Filter by tag:&nbsp;</b>
                    <input type="text" maxLength="255" value={props.filterValues.tag} onChange={(e) => handleChange(e, 'tag')} placeholder="Start Typing"/>
                </FilterDiv>
                <FilterDiv>
                    <b>Sort:&nbsp;</b>
                    <select value={props.filterValues.sort} onChange={(e) => handleChange(e, 'sort')}>
                        <option value="asc">By name ASC</option>
                        <option value="desc">By name DESC</option>
                    </select>                        
                </FilterDiv>
                <FilterDiv>
                    <b>Show&nbsp;</b>
                    <select value={props.filterValues.show} onChange={(e) => handleChange(e, 'show')}>
                        <option value="10">10</option>
                        <option value="20">20</option>
                        <option value="30">30</option>
                        <option value="40">40</option>
                        <option value="50">50</option>
                        <option value="60">60</option>
                        <option value="70">70</option>
                        <option value="80">80</option>
                        <option value="90">90</option>
                        <option value="100">100</option>
                    </select>                        
                    <b>&nbsp;records per page</b>
                </FilterDiv>
            </Wrap>
        </form>
    );
};

export default SearchFilters;