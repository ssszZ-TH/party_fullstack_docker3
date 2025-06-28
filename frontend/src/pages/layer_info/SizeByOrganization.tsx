import React from 'react'
import { useParams } from 'react-router-dom'

function SizeByOrganization() {
  const { paramId } = useParams<{ paramId: string }>()
  return (
    <div>SizeByOrganization {paramId}</div>
  )
}

export default SizeByOrganization