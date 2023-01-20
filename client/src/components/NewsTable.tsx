import React, {
  FC,
  useEffect,
  useRef,
  useState,
} from 'react'
import { query } from '../api/query'
import DataTable from 'react-data-table-component'
import { TableColumn } from 'react-data-table-component/dist/src/DataTable/types'
import { TNewsItem } from '../api/types'
import dayjs from 'dayjs'
import { ExpandableComponent } from './ExpandableComponent'
import { isEmpty } from 'lodash'

const columns: TableColumn<TNewsItem>[] = [
  {
    name: 'Заголовок',
    cell: row => <a className="text-blue-700" href={ row.link } target="_blank">{ row.title }</a>,
  },
  {
    name: 'Дата',
    cell: row => dayjs(row.date).format('YYYY-MM-DD'),
    width: 'fit-content',
  },
  {
    name: 'Текст новости',
    selector: row => row.text,
    wrap: false,
    maxWidth: '500px',
  },
  {
    name: 'Субъекты',
    cell: ({ persons, places }) => (
      <div className="m-0 p-0">
        { persons && <p><b>Политики: </b>{ persons }</p> }
        { places && <p><b>Достопримечательности: </b>{ places }</p> }
      </div>
    ),
  },
]

const NewsTable: FC = () => {
  const [ size, setSize ] = useState(50)
  const { data: news, isLoading } = query.news({ page: 0, size: 99999 })
  const [ search, setSearch ] = useState('')
  const [ newsFiltered, setNewsFiltered ] = useState<TNewsItem[]>([])
  const timerRef = useRef<number>()

  useEffect(() => {
    timerRef.current = setTimeout(() => {
      if ( isEmpty(search) )
        setNewsFiltered(news ?? [])
      else {
        setNewsFiltered((news ?? []).filter(el => {
          return el.text.toLowerCase().includes(search) || el.persons.toLowerCase().includes(search) || el.places.toLowerCase().includes(search)
        }))
      }
    }, 500)
    return () => clearTimeout(timerRef.current)
  }, [ isLoading, search ])

  return <div className="flex flex-col grow">
    <div className="flex justify-center my-2 gap-10">
      <h2 className="cursor-default">Новости</h2>
      <input
        value={ search }
        placeholder="поиск"
        onChange={ e => setSearch(e.currentTarget.value.toLowerCase()) }
        className="border border-2 border-sky-500 rounded px-3 py-1"
      />
    </div>
    { !newsFiltered || isEmpty(newsFiltered)
      ? <div className="flex justify-center">Загрузка...</div>
      : <DataTable
        className="border border-2 border-gray-300 !rounded-xl overflow-hidden"
        data={ newsFiltered ?? [] }
        columns={ columns }
        dense
        striped
        fixedHeader

        paginationRowsPerPageOptions={ [ 10, 20, 50, 200, 500 ] }

        pagination
        paginationPerPage={ size }
        onChangeRowsPerPage={ currentRowsPerPage => setSize(currentRowsPerPage) }

        expandableRows
        expandableRowsComponent={ ExpandableComponent }
        // responsive={ true }
      />
    }

  </div>
}

export default NewsTable


// <Table dark hover responsive size='sm' striped>
// <thead>
//
// </thead>
// </Table>