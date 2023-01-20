import { query } from '../api/query'
import {
  cloneDeep,
  isEmpty,
} from 'lodash'
import React, { Fragment } from 'react'
import { ExpandableRowsComponent } from 'react-data-table-component/dist/src/DataTable/types'
import { TNewsItem } from '../api/types'

export const ExpandableComponent: ExpandableRowsComponent<TNewsItem> = ({ data: { id, text: newsText } }) => {
  const { data: sentences } = query.sentencesByNewsId(id)

  const sentencesSortNormal = sentences?.sort((a, b) => a.start_index - b.start_index) ?? []
  const sentencesSortReverse = cloneDeep(sentencesSortNormal).reverse()
  // const sentencesSortReverse = sentences?.sort((a, b) => b.start_index - a.start_index) ?? []
  const dogsText = sentencesSortReverse
    .reduce<string>((rez, sentence) => rez.substring(0, sentence.start_index) + '@@@' + rez.substring(sentence.start_index + sentence.len), newsText)
    .split('@@@')
    .map(el => el.replace(/(^\s+|\s+$)/g, ''))

  let sentNormalIndex = 0
  const jsxArray: JSX.Element[] = dogsText.flatMap((el, i) => {
    const sentence = sentencesSortNormal[sentNormalIndex++]
    return dogsText.length - 1 !== i
      ? [
        <Fragment key={ Math.random() }>{ el }</Fragment>,
        <>&nbsp;</>,
        <span key={ Math.random() } className={ sentence.tonality == 'Positive' ? 'bg-green-200' : 'bg-red-200' }>{ sentence.sentence }</span>,
        <>&nbsp;</>,
      ]
      : <Fragment key={ Math.random() }>{ el }</Fragment>
  })

  return <div key={ id } className="text-[14px] indent-6 text-justify px-[3vw] py-2">
    {
      isEmpty(sentences) ? newsText : jsxArray
    }
  </div>
}