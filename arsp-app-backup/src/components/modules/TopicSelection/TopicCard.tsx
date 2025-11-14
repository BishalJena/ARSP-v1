import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ExternalLink, TrendingUp, Users } from 'lucide-react'
import type { Topic } from '@/types/topics'

interface TopicCardProps {
  topic: Topic
  onSelect?: (topic: Topic) => void
}

export function TopicCard({ topic, onSelect }: TopicCardProps) {

  const handleClick = () => {
    if (onSelect) {
      onSelect(topic)
    } else {
      // Open in new tab if no handler provided
      window.open(topic.url, '_blank', 'noopener,noreferrer')
    }
  }

  return (
    <Card 
      className="hover:shadow-md transition-shadow cursor-pointer"
      onClick={handleClick}
    >
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <CardTitle className="text-lg line-clamp-2">
              {topic.title}
            </CardTitle>
            {topic.authors && topic.authors.length > 0 && (
              <CardDescription className="mt-2 flex items-center gap-1">
                <Users className="w-3 h-3" />
                <span className="text-xs line-clamp-1">
                  {topic.authors.slice(0, 3).join(', ')}
                  {topic.authors.length > 3 && ` +${topic.authors.length - 3} more`}
                </span>
              </CardDescription>
            )}
          </div>
          <div className="flex flex-col items-end gap-2">
            <Badge variant={topic.impactScore > 70 ? 'default' : 'secondary'}>
              <TrendingUp className="w-3 h-3 mr-1" />
              {topic.impactScore}
            </Badge>
            {topic.year && (
              <span className="text-xs text-muted-foreground">{topic.year}</span>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground line-clamp-3">
          {topic.brief}
        </p>
        <div className="mt-4 flex items-center justify-between">
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            {topic.citationCount !== undefined && (
              <span>{topic.citationCount} citations</span>
            )}
            <Badge variant="outline" className="text-xs">
              {topic.source === 'semantic_scholar' ? 'Semantic Scholar' : 'arXiv'}
            </Badge>
          </div>
          <ExternalLink className="w-4 h-4 text-muted-foreground" />
        </div>
      </CardContent>
    </Card>
  )
}
