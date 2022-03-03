import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { Wrap } from './styles/styled-paginator';
import ReactPaginate from 'react-paginate';
import 'bootstrap/dist/css/bootstrap.min.css';

const Paginator = (props) => {

    const PaginatedItems = () => {
        const [pageCount, setPageCount] = useState(0);
        const [forcePage, setForcePage] = useState(0);

        useEffect(() => {
            setPageCount(Math.ceil(props.itemsLength / props.itemsPerPage));
            setForcePage(props.offset / props.itemsPerPage);
        }, [props.offset, props.itemsPerPage]);

        const handlePageClick = (event) => {
            const newOffset = (event.selected * props.itemsPerPage) % props.itemsLength;
            props.onUpdatedOffset(newOffset);
            setForcePage(event.selected);
        };

        return (
            <Wrap>
                <ReactPaginate
                    nextLabel="Next >"
                    onPageChange={handlePageClick}
                    pageRangeDisplayed={3}
                    marginPagesDisplayed={2}
                    pageCount={pageCount}
                    previousLabel="< Previous"
                    pageClassName="page-item"
                    pageLinkClassName="page-link"
                    previousClassName="page-item"
                    previousLinkClassName="page-link"
                    nextClassName="page-item"
                    nextLinkClassName="page-link"
                    breakLabel="..."
                    breakClassName="page-item"
                    breakLinkClassName="page-link"
                    containerClassName="pagination"
                    activeClassName="active"
                    renderOnZeroPageCount={null}
                    forcePage={(pageCount < 0) ? null : forcePage}
                />
            </Wrap>
        );
    }


    return (
        <Wrap>
            <PaginatedItems />
        </Wrap>
    );

};

export default Paginator;