<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="div[@type='section']">
<div>
<xsl:copy-of select="./@*"/>
<xsl:attribute name="n">
<xsl:value-of select="parent::div[@type='pāda']/parent::div[@type='adhyāya']/@n"/>
<xsl:text>_</xsl:text>
<xsl:value-of select="parent::div[@type='pāda']/@n"/>
<xsl:text>_</xsl:text>
<xsl:value-of select="child::ab[@type='sūtra']/@n"/>
</xsl:attribute>
<xsl:copy-of select="./node()"/>
</div>
</xsl:template>

</xsl:stylesheet>