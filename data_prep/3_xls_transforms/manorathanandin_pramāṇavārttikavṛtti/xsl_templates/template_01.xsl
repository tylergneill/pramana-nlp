<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="teiHeader" />

<xsl:template match="comment()" />

<xsl:template match="front" />

<xsl:template match="note" />

<xsl:template match="sic" />

<xsl:template match="corr">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="anchor" />

<xsl:template match="ref[text()]">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="ref[not(text())]">
<xsl:text>(</xsl:text><xsl:value-of select="@cRef"/><xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="//l/quote">
<xsl:text>"</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text>
</xsl:template>

</xsl:stylesheet>