'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'

import Searchbar from '@/components/home/Searchbar'

const HomePage = () => {
  const [recommendations, setRecommendations] = useState([])

  const [results, setResults] = useState([])

  useEffect(() => {
    const getResults = async () => {
      try {
        recommendations.forEach(async (recommendation) => {
          const response = await fetch(`https://api.themoviedb.org/3/search/movie?api_key=${process.env.NEXT_PUBLIC_TMDB_API_KEY}&query=${recommendation}`)

          if (response.ok) {
            const data = await response.json()

            let recommendationMovieData = data.results.find((result) => result.original_title.toLowerCase() === recommendation.toLowerCase()) || { original_title: 'Not Mentioned', poster_path: 'Not Mentioned' }

            setResults((previousResults) => [...previousResults, recommendationMovieData])
          }
        })
      } catch (error) {
        setResults([])
      }
    }

    getResults()
  }, [recommendations])

  return (
    <div className="py-16 px-6 md:px-20 lg:px-32 h-full">
      <Searchbar setRecommendations={setRecommendations} setResults={setResults} />

      {
        results.length > 0 && (
          <div className="mt-16 space-y-16">
            <h1 className="text-white text-center leading-none text-2xl md:text-3xl font-bold">Recommendations ({results.length} Results)</h1>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-x-6 gap-y-10">

              {results.map((result, index) => (
                <Link key={index} href={`/movies/${result.id}`}>
                  {/* <h1 className="font-bold text-2xl text-white">{result.original_title}</h1> */}
                  <Image className="w-full object-cover bg-white" src={`https://image.tmdb.org/t/p/original${result.poster_path}`} alt={result.original_title} fill={true} />
                </Link>
              ))}

            </div>
          </div>
        )
      }

    </div >
  )
}

export default HomePage