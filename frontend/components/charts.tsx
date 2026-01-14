import * as React from "react"
import * as RechartsPrimitive from "recharts"
import { cn } from "@/lib/utils"

// const COLORS = [
//   "hsl(var(--chart-1))",
//   "hsl(var(--chart-2))",
//   "hsl(var(--chart-3))",
//   "hsl(var(--chart-4))",
//   "hsl(var(--chart-5))",
// ]

const COLORS = [
  "#4a8bc2", // Blue - matches your gradient
  "#2a5a8a", // Darker blue
  "#5ca3d8", // Lighter blue
  "#1e4a6f", // Deep blue
  "#3d7ba8", // Medium blue
]

type ChartConfig = {
  [k in string]: {
    label?: React.ReactNode
    color?: string
  }
}

const ChartContext = React.createContext<ChartConfig | null>(null)

function useChart() {
  const context = React.useContext(ChartContext)
  if (!context) {
    throw new Error("useChart must be used within a <ChartContainer>")
  }
  return context
}

const ChartContainer = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    config: ChartConfig
    children: React.ComponentProps<typeof RechartsPrimitive.ResponsiveContainer>["children"]
  }
>(({ id, className, children, config, ...props }, ref) => {
  const uid = React.useId()
  const chartId = `chart-${id || uid.replace(/:/g, "")}`

  return (
    <ChartContext.Provider value={config}>
      <div
        ref={ref}
        className={cn("flex aspect-auto h-px w-full", className)}
        {...props}
      >
        <RechartsPrimitive.ResponsiveContainer width="100%" height="100%">
          {children}
        </RechartsPrimitive.ResponsiveContainer>
      </div>
    </ChartContext.Provider>
  )
})
ChartContainer.displayName = "ChartContainer"

const ChartTooltip = RechartsPrimitive.Tooltip

const ChartTooltipContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    active?: boolean
    payload?: Array<any>
    label?: string | number
  }
>(({ active, payload, label, className, ...props }, ref) => {
  if (!active || !payload || payload.length === 0) {
    return null
  }

  return (
    <div
      ref={ref}
      className={cn(
        "rounded-lg border border-border bg-background px-2 py-1.5 text-sm shadow-md",
        className
      )}
      {...props}
    >
      <div className="font-semibold">{label}</div>
      <div className="space-y-1">
        {payload.map((item, index) => (
          <div key={`${item.dataKey}-${index}`} className="text-xs">
            <span
              className="mr-2 inline-block h-2 w-2 rounded-full"
              style={{
                backgroundColor: item.color || COLORS[index % COLORS.length],
              }}
            />
            {item.name}: {item.value}
          </div>
        ))}
      </div>
    </div>
  )
})
ChartTooltipContent.displayName = "ChartTooltipContent"

export { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig, COLORS }