import { cn } from "@/lib/utils"

interface BentoGridProps {
  children: React.ReactNode
  className?: string
}

interface BentoGridItemProps {
  children: React.ReactNode
  className?: string
  colSpan?: number
  rowSpan?: number
}

export function BentoGrid({ children, className }: BentoGridProps) {
  return (
    <div
      className={cn(
        "grid auto-rows-[minmax(350px,auto)] grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3",
        className
      )}
    >
      {children}
    </div>
  )
}

export function BentoGridItem({ 
  children, 
  className, 
  colSpan = 1, 
  rowSpan = 1 
}: BentoGridItemProps) {
  return (
    <div
      className={cn(
        "group relative overflow-hidden rounded-xl border border-gray-700/50 bg-[#0a0e17]/60 backdrop-blur-sm p-6 transition-all hover:shadow-xl hover:shadow-[#4a8bc2]/10 hover:border-[#4a8bc2]/30 min-h-[350px]",
        colSpan === 2 && "md:col-span-2",
        colSpan === 3 && "lg:col-span-3",
        rowSpan === 2 && "md:row-span-2 min-h-[700px]",
        className
      )}
    >
      {children}
    </div>
  )
}