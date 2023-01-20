export type TApiJavaParams = {
  page: number
  size: number
}

// export type TApiCount = {
//   newsCount: number
//   sentencesCount: number
// }

export type TNewsItem = {
  readonly id: string
  title: string
  date: string
  link: string
  text: string
  persons: string
  places: string
}

export type TTonality = 'Positive' | 'Negative'
export type TJavaSentenceItem = {
  readonly id: string
  detected: string
  link: string
  sentence: string
  title: string
  tonality: TTonality
  type: 'Person' | 'Place'
}

export type TPythonSentenceItem = {
  _id: string
  title: string
  link: string
  detected: string
  sentence: string
  type: string
  tonality: string
  start_index: number
  len: number
}

export type TSynonymItem = {
  word: string
  similarity: number
}

export type TSynonymsNotFound = {
  error: string
}