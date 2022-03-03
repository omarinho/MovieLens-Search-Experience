import { useContext, useState, useEffect } from "react";
import SearchFilters from '../components/SearchFilters';
import Paginator from '../components/Paginator';
import './styles/home.css';
import useFetch from "../hooks/useFetch";
import { ConfigContext } from '../contexts/ConfigContext';
import { faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const mimimumCharactersForTextFields = 3;

const Home = () => {
  const apiServer = useContext(ConfigContext);
  const [filterValues, setFilterValues] = useState({
    title: '',
    genre: '',
    tag: '',
    sort: 'asc',
    show: '30',
    refetch: '',
  });
  const [offset, setOffset] = useState(0);
  let titleForQuery = (filterValues.title.length >= mimimumCharactersForTextFields) ? filterValues.title : '';
  let tagForQuery = (filterValues.tag.length >= mimimumCharactersForTextFields) ? filterValues.tag : '';
  const queryString = `title=${titleForQuery}&genre=${filterValues.genre}&tag=${tagForQuery}&sort=${filterValues.sort}&show=${filterValues.show}`
  const queryStringWithOffset = queryString + `&offset=${offset}`;
  const [data] = useFetch(apiServer + `/api/v1.0/movies/?${queryStringWithOffset}`);
  const [genres] = useFetch(apiServer + `/api/v1.0/genres/`);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [data]);

  const UpdateSearchFilters = (value, property) => {
    setOffset(0);
    switch(property) {
      case 'title':
        setFilterValues(previousState => {
          return { ...previousState, title: value }
        });
        break;
      case 'genre':
        setFilterValues(previousState => {
          return { ...previousState, genre: value }
        });
        break;
      case 'tag':
        setFilterValues(previousState => {
          return { ...previousState, tag: value }
        });
        break;
      case 'sort':
        setFilterValues(previousState => {
          return { ...previousState, sort: value }
        });
        break;
      case 'show':
        setFilterValues(previousState => {
          return { ...previousState, show: value }
        });
        break;
    }
  }

  const UpdateOffset = (value) => {
    setOffset(value);
  }

  return (
    <div className="wrap">
      <SearchFilters 
        filterValues={filterValues} 
        onUpdatedFilters={UpdateSearchFilters} 
        minimumChar={mimimumCharactersForTextFields}
        genres={genres}
      />
      <div>
        <table className="resultsTable">
          <thead>
            <tr>
              <th className="resultsTh"><b>Title</b></th>
              <th className="resultsTh"><b>Genres</b></th>
              <th className="resultsTh textCenter"><b>Average Rating</b></th>
              <th className="resultsTh"><b>Tags</b></th>
              <th className="resultsTh"></th>
              <th className="resultsTh"></th>
            </tr>
          </thead>
          <tbody>
            {data && data.map((item) => {
              return(
                <tr key={item.movie_id}>
                  <td className="resultsTd title">{item.title}</td>
                  <td className="resultsTd" title={item.genres.join(' | ')}>{item.genres.length > 0 ? item.genres.join(' | ').substring(0, 50) + "..." : "-"}</td>
                  <td className="resultsTd textCenter">{parseFloat(item.average_rating).toFixed(1)}</td>
                  <td className="resultsTd" title={item.tags.join(', ')}>{item.tags.length > 0 ? item.tags.join(', ').substring(0, 50) + "..." : "-"}</td>
                  <td className="resultsTd">
                    <a href={"https://www.imdb.com/title/tt" + item.imdb_id + "/"} target="_blank">See in IMDB</a>
                    &nbsp;<FontAwesomeIcon icon={faExternalLinkAlt} />
                  </td>
                  <td className="resultsTd">
                    <a href={"https://www.themoviedb.org/movie/" + item.tmdb_id} target="_blank">See in TMDB</a>
                    &nbsp;<FontAwesomeIcon icon={faExternalLinkAlt} />
                  </td>
                </tr>
              );
            })}
            {data && data.length == 0 &&
              <tr>
                <td colspan="6" align="center">
                  <br/>
                  <h3>No movies found with these filters.</h3>
                </td>
              </tr>
            }
          </tbody>
        </table>
      </div>
      {data && data.length > 0 &&
        <Paginator 
          itemsPerPage={filterValues.show} 
          itemsLength={data[0].total} 
          offset={offset}
          onUpdatedOffset={UpdateOffset}
        />
      }
    </div>
  );
};

export default Home;