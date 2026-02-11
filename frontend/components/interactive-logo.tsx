"use client"

import { useState, useEffect } from "react"
import "../styles/interactive-logo.css"

export function InteractiveLogo() {
  const [hoveredTile, setHoveredTile] = useState<string | null>(null)
  const [appearingTiles, setAppearingTiles] = useState<Set<string>>(new Set())
  const [disappearingTiles, setDisappearingTiles] = useState<Set<string>>(new Set())

  // Define letter patterns (5x5 grid for each letter)
  const letterPatterns: Record<string, boolean[][]> = {
    M: [
      [true, false, false, false, true],
      [true, true, false, true, true],
      [true, false, true, false, true],
      [true, false, false, false, true],
      [true, false, false, false, true],
    ],
    O: [
      [false, true, true, true, false],
      [true, false, false, false, true],
      [true, false, false, false, true],
      [true, false, false, false, true],
      [false, true, true, true, false],
    ],
    S: [
      [false, true, true, true, false],
      [true, false, false, false, false],
      [false, true, true, true, false],
      [false, false, false, false, true],
      [false, true, true, true, false],
    ],
    A: [
      [false, true, true, true, false],
      [true, false, false, false, true],
      [true, false, false, false, true],
      [true, true, true, true, true],
      [true, false, false, false, true],
    ],
    I: [
      [false, false, true, false, false],
      [false, false, true, false, false],
      [false, false, true, false, false],
      [false, false, true, false, false],
      [false, false, true, false, false],
    ],
    C: [
      [false, true, true, true, false],
      [true, false, false, false, false],
      [true, false, false, false, false],
      [true, false, false, false, false],
      [false, true, true, true, false],
    ],
  }

  // Zigzag layout: MO (top-left), SA (middle-right), IC (bottom-left)
  const letterPositions: Record<string, { row: number; col: number }> = {
    M: { row: 0, col: 0 },
    O: { row: 0, col: 1 },
    S: { row: 0, col: 2 },
    A: { row: 1, col: 1 },
    I: { row: 1, col: 2 },
    C: { row: 1, col: 3 },
  }

  const tileSize = 32
  const gapSize = 2
  const tileSpacing = tileSize + gapSize
  const letterSpacing = tileSpacing * 5 + 30 // Space between letters

  const generateTileId = (letter: string, tileRow: number, tileCol: number) => {
    return `${letter}-${tileRow}-${tileCol}`
  }

  // Animation effect on mount
  useEffect(() => {
    const animateTiles = () => {
      const tiles: string[] = []
      
      // Collect all active tiles in order (left to right, top to bottom, following zigzag)
      const letterOrder = ['M', 'O', 'S', 'A', 'I', 'C']
      
      letterOrder.forEach((letter) => {
        const pattern = letterPatterns[letter]
        pattern.forEach((row, tileRow) => {
          row.forEach((active, tileCol) => {
            if (active) {
              tiles.push(generateTileId(letter, tileRow, tileCol))
            }
          })
        })
      })

      // Animate tiles appearing sequentially
      tiles.forEach((tileId, index) => {
        setTimeout(() => {
          setAppearingTiles((prev) => new Set(prev).add(tileId))
          
          // Remove appearing state after animation
          setTimeout(() => {
            setAppearingTiles((prev) => {
              const newSet = new Set(prev)
              newSet.delete(tileId)
              return newSet
            })
          }, 1000) // Duration of appear animation
        }, index * 80) // Stagger tiles by 80ms
      })

      // After all tiles appear, animate them disappearing
      setTimeout(() => {
        tiles.forEach((tileId, index) => {
          setTimeout(() => {
            setDisappearingTiles((prev) => new Set(prev).add(tileId))
            
            // Remove disappearing state after animation
            setTimeout(() => {
              setDisappearingTiles((prev) => {
                const newSet = new Set(prev)
                newSet.delete(tileId)
                return newSet
              })
            }, 1000) // Duration of disappear animation
          }, index * 80) // Stagger tiles by 80ms
        })
      }, tiles.length * 80 + 800) // Wait for all tiles to appear, then start disappearing

      // Restart animation
      setTimeout(animateTiles, tiles.length * 80 + tiles.length * 80 + 2000)
    }

    animateTiles()
  }, [])

  return (
    <div className="interactive-logo">
      <svg
        viewBox="0 0 750 450"
        className="logo-svg"
        preserveAspectRatio="xMidYMid meet"
      >
        {Object.entries(letterPatterns).map(([letter, pattern]) => {
          const position = letterPositions[letter]
          const startX = position.col * letterSpacing
          const startY = position.row * letterSpacing

            return (
              <g key={letter}>
                {pattern.map((row, tileRow) =>
                  row.map((active, tileCol) => {
                    const tileId = generateTileId(letter, tileRow, tileCol)
                    const x = startX + tileCol * tileSpacing
                    const y = startY + tileRow * tileSpacing
                    const isHovered = hoveredTile === tileId

                    return (
                      <g
                        key={tileId}
                        onMouseEnter={() => active && setHoveredTile(tileId)}
                        onMouseLeave={() => setHoveredTile(null)}
                        style={{ cursor: active ? "pointer" : "default" }}
                      >
                        {/* Tile background */}
                        <rect
                          x={x}
                          y={y}
                          width={tileSize}
                          height={tileSize}
                          fill={active ? (isHovered ? "#4a8bc2" : "#2d5a8f") : "transparent"}
                          stroke={active ? (isHovered ? "#7aa8d4" : "#4a7daa") : "transparent"}
                          strokeWidth="1"
                          rx="2"
                          className={`mosaic-tile-svg ${active ? "active" : "inactive"} ${
                            isHovered ? "hovered" : ""
                          } ${appearingTiles.has(tileId) ? "appearing" : ""} ${
                            disappearingTiles.has(tileId) ? "disappearing" : ""
                          }`}
                          style={{
                            filter: isHovered
                              ? "drop-shadow(0 4px 12px rgba(74, 139, 194, 0.6))"
                              : active
                              ? "drop-shadow(0 2px 4px rgba(74, 139, 194, 0.3))"
                              : "none",
                            transition: appearingTiles.has(tileId) || disappearingTiles.has(tileId) ? "none" : "all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
                            transform: isHovered ? "translate(0, -3px)" : "translate(0, 0)",
                            transformOrigin: `${x + tileSize / 2}px ${y + tileSize / 2}px`,
                          }}
                        />
                        {/* Highlight on hover */}
                        {isHovered && (
                          <rect
                            x={x + 1}
                            y={y + 1}
                            width={tileSize - 2}
                            height={tileSize - 2}
                            fill="none"
                            stroke="#7aa8d4"
                            strokeWidth="1.5"
                            rx="1.5"
                            opacity="0.6"
                          />
                        )}
                      </g>
                    )
                  })
                )}
              </g>
            )
        })}
      </svg>
    </div>
  )
}
