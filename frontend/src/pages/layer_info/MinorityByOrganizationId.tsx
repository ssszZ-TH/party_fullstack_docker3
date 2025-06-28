import React from 'react'
import { useParams } from 'react-router-dom'

function MinorityByOrganizationId() {
  const { paramId } = useParams<{ paramId: string }>()
  return (
    <div>MinorityByOrganizationId {paramId}</div>
  )
}

export default MinorityByOrganizationId