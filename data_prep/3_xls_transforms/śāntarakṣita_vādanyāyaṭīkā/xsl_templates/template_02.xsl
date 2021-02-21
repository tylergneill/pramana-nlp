<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="note[@type='correction']">
<xsl:text>(</xsl:text><xsl:value-of select="."/><xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="ref[@target]">
<xsl:text>〈f.</xsl:text><xsl:value-of select="."/><xsl:text>〉</xsl:text>
</xsl:template>

<xsl:template match="ref[@cRef]">
<xsl:text>(</xsl:text><xsl:value-of select="."/><xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="hi">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="foreign">
<xsl:text>(</xsl:text><xsl:value-of select="."/><xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="lb[@break='no']" />

</xsl:stylesheet>