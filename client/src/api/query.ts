import {
  useMutation,
  useQuery,
} from '@tanstack/react-query'
import {
  TApiJavaParams,
  TNewsItem,
  TJavaSentenceItem,
  TSynonymItem,
  TTonality,
  TPythonSentenceItem,
  TSynonymsNotFound,
} from './types'
import axios from 'axios'

const javaURL = import.meta.env.VITE_API_HOST
  ? `http://${ import.meta.env.VITE_API_HOST }:${ import.meta.env.VITE_API_PORT }`
  : 'http://localhost:8080'

const pythonURL = import.meta.env.VITE_PYTHON_HOST
  ? `http://${ import.meta.env.VITE_PYTHON_HOST }:${ import.meta.env.VITE_PYTHON_PORT }`
  : 'http://localhost:8081'


export const query = {
  news: ({ page, size }: TApiJavaParams) => useQuery({
    queryKey: [ 'news' ],
    queryFn: async () => (await axios.get<TNewsItem[]>(`${ javaURL }/news?page=${ page }&size=${ size }`)).data,
  }),
  newsTotal: () => useQuery({
    queryKey: [ 'newsTotal' ],
    queryFn: async () => (await axios.get<number>(`${ javaURL }/news/count`)).data,
  }),
  sentencesByNewsId: (newsItemId: string) => useQuery({
    queryKey: [ `sentencesByNewsId${ newsItemId }` ],
    queryFn: async () => (await axios.get<TPythonSentenceItem[]>(`${ pythonURL }/news-tonalities?news_id=${ newsItemId }`)).data,
  }),
  // sentences: ({ page, size }: TApiJavaParams) => useQuery({
  //   queryKey: [ 'sentences' ],
  //   queryFn: async () => (await axios.get<TSentenceItem[]>(`${ javaURL }/sentences?page=${ page }&size=${ size }`)).data,
  // }),
  // sentencesTotal: () => useQuery({
  //   queryKey: [ 'sentencesTotal' ],
  //   queryFn: async () => (await axios.get<number>(`${ javaURL }/sentences/count`)).data,
  // }),
  synonyms: () => useMutation({
    mutationKey: [ 'synonyms' ],
    mutationFn: async (word: string) => (await axios.get<TSynonymItem[] | TSynonymsNotFound>(`${ pythonURL }/synonyms?word=${ word }`)).data,
  }),
  tonality: () => useMutation({
    mutationKey: [ 'tonality' ],
    mutationFn: async (sentence: string) => (await axios.get<TTonality>(`${ pythonURL }/tonality?sentence=${ sentence }`)).data,
  }),
}
