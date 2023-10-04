'use client'

import { Search } from 'lucide-react'
import * as z from 'zod'
import { set, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useState, useEffect } from 'react'
import { twMerge } from 'tailwind-merge'
import { toast } from 'react-hot-toast'
import useDebounce from '@/hooks/useDebounce'

const schema = z.object({
    query: z.string().nonempty().refine((value) => !/^\s*$/.test(value)),
})

const Searchbar = ({
    setRecommendations,
    setResults,
}) => {
    const { register, handleSubmit, watch, setValue } = useForm({
        resolver: zodResolver(schema),
        defaultValues: {
            query: '',
        },
    })

    const [suggestions, setSuggestions] = useState([])

    const debouncedQuery = useDebounce(watch('query'), 1000)

    console.log(debouncedQuery)

    useEffect(() => {
        const getSuggestions = async () => {
            try {
                const response = await fetch('http://localhost:8001/movies')

                if (response.ok) {
                    const data = await response.json()

                    const suggestionData = debouncedQuery !== '' && data.filter((movie) => movie.toLowerCase().includes(debouncedQuery.toLowerCase()))

                    setSuggestions(suggestionData)
                }
            } catch (error) {
                setSuggestions([])
            }
        }

        getSuggestions()
    }, [debouncedQuery])

    const [isLoading, setIsLoading] = useState(false)

    const onSubmit = async (values) => {
        setSuggestions([])

        try {
            setIsLoading(true)

            const response = await fetch(`http://localhost:8001/movies/recommendations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ movie: values.query }),
            })

            if (response.ok) {
                const data = await response.json()

                setRecommendations(data)
            }
        } catch (error) {
            toast.error('Something went wrong. Please try again later.')
        } finally {
            setIsLoading(false)
        }
    }

    const [isSuggestionContainerOpen, setIsSuggestionContainerOpen] = useState(true)

    return (
        <div className="md:max-w-md mx-auto px-6 relative">
            <div>
                <form noValidate onSubmit={handleSubmit(onSubmit)}>
                    <div className="p-2 rounded-full bg-black bg-opacity-95 flex items-center ring-2 ring-neutral-600 focus-within:ring-2 focus-within:ring-red-900 ring-opacity-50">
                        <input className={twMerge('flex-1 px-4 font-light text-sm bg-transparent focus:outline-none focus-visible:outline-none mr-2 text-neutral-400', isLoading && 'opacity-50 cursor-not-allowed')} disabled={isLoading} {...register('query')} />
                        <button className={twMerge('cursor-pointer rounded-full p-2 bg-red-600 hover:bg-red-700', isLoading && 'opacity-50 cursor-not-allowed')} type="submit" disabled={isLoading} onClick={() => setResults([])}>
                            <Search className="w-4 h-4" />
                        </button>
                    </div>
                </form>
            </div>

            {suggestions.length > 0 && (
                <div className={twMerge('overflow-hidden rounded-lg bg-black max-h-[50vh] overflow-y-auto absolute left-6 right-6 mt-6 z-50 border border-neutral-900', isSuggestionContainerOpen ? 'block' : 'hidden')}>

                    {suggestions.map((suggestion, index) => (
                        <p key={index} className="py-2 px-4 text-neutral-400 hover:bg-neutral-900 cursor-pointer truncate" onClick={() => {
                            setValue('query', suggestion)
                            setIsSuggestionContainerOpen(false)
                        }}>{suggestion}</p>
                    ))}

                </div>
            )}
        </div>
    )
}

export default Searchbar