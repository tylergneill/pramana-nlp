<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
 <xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
 </xsl:copy>
</xsl:template>

<xsl:template match="teiHeader" />

<xsl:template match="back" />

<xsl:template match="front" />

<xsl:template match="comment()" />

<xsl:template match="anchor" />

<xsl:template match="note" />

<xsl:template match="persName">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="rdg" />

<xsl:template match="sic" />

<xsl:template match="corr">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="gap" />

<xsl:template match="ref|s" />

<xsl:template match="hi[q]">
<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>
</xsl:template>


</xsl:stylesheet>
