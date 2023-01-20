import React, {
  FC,
  useState,
} from 'react'
import { query } from '../api/query'
import DataTable from 'react-data-table-component'
import { TableColumn } from 'react-data-table-component/dist/src/DataTable/types'
import { TSynonymItem } from '../api/types'
import {
  isArray,
  round,
} from 'lodash'

const columns: TableColumn<TSynonymItem>[] = [
  {
    name: '№',
    cell: (_, rowIndex) => rowIndex + 1,
    right: true,
    width: '50px',
    grow: 0,
  },
  {
    name: 'Сходство',
    cell: row => round(row.similarity * 100, 2) + ' %',
    right: true,
    grow: 0,
  },
  {
    name: 'Слово',
    cell: row => row.word,
    grow: 1,
  },
]

const TonalityBlock: FC = () => {
  const [ word, setWord ] = useState('')
  const { mutateAsync, data, isLoading } = query.synonyms()

  return <div className="w-[30vw] mx-auto flex flex-col grow">
    {/*<h2 className="cursor-default">Поиск синонимов</h2>*/ }
    <div className="flex justify-center my-2 gap-2">
      <input
        value={ word }
        placeholder="Поиск синонимов для ..."
        onKeyDown={ e => {
          if ( isLoading ) return
          return e.key === 'Enter' && mutateAsync(word)
        } }
        onChange={ e => setWord(e.currentTarget.value) }
        className="border border-2 border-sky-500 rounded px-3 py-1"
      />
      <button
        disabled={ isLoading }
        onClick={ () => mutateAsync(word) }
        className="bg-sky-500 hover:bg-sky-600 text-white rounded px-3 py-1"
      >Поиск
      </button>
    </div>
    {
      isLoading
        ? <p className="flex justify-center">Загрузка...</p>
        : data
          ? isArray(data)
            ? <DataTable
              className="border border-2 border-gray-300 !rounded-xl overflow-hidden"
              columns={ columns }
              data={ data ?? [] }
              fixedHeader
              // pagination
              // paginationPerPage={ 30 }
              // paginationRowsPerPageOptions={ [ 30 ] }
              responsive
              dense
              striped
            />
            : <p className="flex justify-center">Данного слова нет в словаре!</p>
          : <p className="flex justify-center">Введите запрос</p>
    }
  </div>
}

export default TonalityBlock