<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="supplied">
<xsl:text>{</xsl:text><xsl:value-of select="node()"/><xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="//quote/hi">
<xsl:value-of select="node()"/>
</xsl:template>

<xsl:template match="//add/hi">
<xsl:text>"</xsl:text>
<xsl:value-of select="node()"/>
<xsl:text>"</xsl:text>
</xsl:template>

<xsl:template match="//hi/quote">
<xsl:value-of select="node()"/>
<xsl:text>(</xsl:text>
<xsl:value-of select="@sameAs"/>
<xsl:text>)</xsl:text>
</xsl:template>

</xsl:stylesheet>